#!/usr/bin/env python3
"""Build the Hugo site and verify its repository and generated output."""

from __future__ import annotations

import hashlib
import json
import os
import posixpath
import re
import struct
import subprocess
import tempfile
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_TITLE = "工程師的摳頂人生"
HUGO_BIN = os.environ.get("CFLIEN_HUGO_BIN", "hugo")
HUGO_VERSION = "0.164.0"
SENSITIVE_SETTING = "ALGOLIA_" + "ADMIN_KEY"
PREVIEW_SUFFIX = "-preview"
LOVEIT_VERSION = "v0.3.1"
LOVEIT_COMMIT = "0349869aa8aa8a09ca44c648da7a31618d45cc1d"
FONTAWESOME_VERSION = "7.3.1"
TYPEIT_VERSION = "8.8.7"
SIMPLE_ICONS_VERSION = "16.27.0"
EMOJI_DATASOURCE_GOOGLE_VERSION = "16.0.0"
LUNR_LANGUAGES_VERSION = "1.20.0"
LUNR_LANGUAGE_HASHES = {
    "assets/lib/lunr/lunr.stemmer.support.js": (
        "4b4c8cc2fd10dc37e4b33b57fc73659f8df833803c7d04bd84e53f01b16add86"
    ),
    "assets/lib/lunr/lunr.zh.js": (
        "25df40afa6898ca07982f7f29039a6698984fc544eb94702a2f1174924fbb882"
    ),
}


def post_cover_urls() -> dict[str, str]:
    covers: dict[str, str] = {}
    for post_path in sorted((REPO_ROOT / "content/posts").glob("*.md")):
        post_text = post_path.read_text()
        match = re.search(
            r'''^featuredImage:\s*["']?([^"']+)["']?\s*$''',
            post_text,
            re.MULTILINE,
        )
        require(match is not None, f"{post_path.name} has no featured image")
        cover_url = match.group(1)
        expected_url = f"/images/covers/{post_path.stem}.png"
        require(
            cover_url == expected_url,
            f"{post_path.name} uses an unexpected featured image",
        )
        cover_path = REPO_ROOT / "static" / cover_url.lstrip("/")
        require(cover_path.is_file(), f"{post_path.name} cover image is missing")
        require(cover_path.stat().st_size > 0, f"{post_path.name} cover image is empty")
        png_header = cover_path.read_bytes()[:24]
        require(
            png_header.startswith(b"\x89PNG\r\n\x1a\n") and len(png_header) == 24,
            f"{post_path.name} cover image is not a valid PNG",
        )
        width, height = struct.unpack(">II", png_header[16:24])
        require(
            width >= 1200 and height >= 630 and width / height >= 1.8,
            f"{post_path.name} cover image is not a high-resolution landscape image",
        )
        for extension in (".avif", ".webp"):
            variant_path = cover_path.with_suffix(extension)
            require(
                variant_path.is_file(),
                f"{post_path.name} {extension[1:].upper()} cover image is missing",
            )
            require(
                0 < variant_path.stat().st_size < cover_path.stat().st_size,
                f"{post_path.name} {extension[1:].upper()} cover is not optimized",
            )
            variant_header = variant_path.read_bytes()[:32]
            if extension == ".avif":
                require(
                    b"ftypavif" in variant_header,
                    f"{post_path.name} cover image is not a valid AVIF",
                )
            else:
                require(
                    variant_header.startswith(b"RIFF")
                    and variant_header[8:12] == b"WEBP",
                    f"{post_path.name} cover image is not a valid WebP",
                )
        for extension in (".avif", ".webp"):
            preview_path = cover_path.with_name(
                f"{cover_path.stem}{PREVIEW_SUFFIX}{extension}"
            )
            full_path = cover_path.with_suffix(extension)
            require(
                preview_path.is_file(),
                f"{post_path.name} {extension[1:].upper()} preview cover is missing",
            )
            require(
                0 < preview_path.stat().st_size < full_path.stat().st_size,
                f"{post_path.name} {extension[1:].upper()} preview cover is not smaller than the full cover",
            )
        covers[post_path.name] = cover_url

    require(covers, "no blog posts were found")
    require(
        len(set(covers.values())) == len(covers),
        "blog posts do not have unique cover images",
    )
    return covers


def _front_matter_value(post_path: Path, key: str) -> str:
    match = re.search(
        rf"""^{key}:\s*["']?([^"'\n]+?)["']?\s*$""",
        post_path.read_text(),
        re.MULTILINE,
    )
    require(match is not None, f"{post_path.name} has no {key} in its front matter")
    return match.group(1)


def post_date(post_name: str) -> str:
    return _front_matter_value(REPO_ROOT / "content/posts" / post_name, "date")


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag not in {"a", "link", "script", "img", "source"}:
            return
        attribute_name = "href" if tag in {"a", "link"} else "src"
        for name, value in attrs:
            if name == attribute_name and value:
                self.links.append(value)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def tracked_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.splitlines()


def verify_repository() -> None:
    forbidden_files = {
        "netlify.toml",
        "package.json",
        "package-lock.json",
        "layouts/_default/list.algolia.json",
    }
    existing_forbidden = sorted(
        file_name for file_name in forbidden_files if (REPO_ROOT / file_name).exists()
    )
    require(
        not existing_forbidden,
        f"obsolete deployment files remain: {', '.join(existing_forbidden)}",
    )

    tracked = tracked_files()
    generated = sorted(
        file_name
        for file_name in tracked
        if (REPO_ROOT / file_name).exists()
        and (
            file_name == "public"
            or file_name.startswith("public/")
            or file_name == "resources"
            or file_name.startswith("resources/")
        )
    )
    require(not generated, "generated public/resources files are still tracked")

    config_text = (REPO_ROOT / "config.toml").read_text()
    config = tomllib.loads(config_text)
    require(
        "algolia" not in json.dumps(config).lower(),
        "Algolia configuration remains",
    )
    require(
        SENSITIVE_SETTING not in "\n".join(
            (REPO_ROOT / file_name).read_text(errors="ignore")
            for file_name in tracked
            if (REPO_ROOT / file_name).is_file()
        ),
        "Algolia admin key remains in tracked files",
    )

    require(config.get("title") == SITE_TITLE, "global site title is not branded")
    languages = config.get("languages", {})
    require("en" not in languages, "empty English site remains enabled")
    require(set(languages) == {"zh-tw"}, "unexpected language configuration")
    language = languages["zh-tw"]
    require(language.get("locale") == "zh-TW", "language locale is not current")
    require(language.get("label") == "正體中文", "language label is not current")
    search = language.get("params", {}).get("search", {})
    require(search.get("type") == "lunr", "Lunr search is not enabled")
    post_cover_urls()

    hugo_version_output = subprocess.run(
        [HUGO_BIN, "version"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    require(
        f"hugo v{HUGO_VERSION}" in hugo_version_output,
        f"Hugo {HUGO_VERSION} is required",
    )

    theme_commit = subprocess.run(
        ["git", "-C", "themes/LoveIt", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    require(
        theme_commit == LOVEIT_COMMIT,
        f"LoveIt {LOVEIT_VERSION} is not checked out",
    )

    middleware_path = REPO_ROOT / "functions/_middleware.js"
    require(middleware_path.is_file(), "pages.dev redirect middleware is missing")
    require(
        ".pages.dev" in middleware_path.read_text() and "301" in middleware_path.read_text(),
        "pages.dev redirect middleware does not redirect pages.dev permanently",
    )
    subprocess.run(
        ["node", str(REPO_ROOT / "scripts/test_pages_dev_redirect.mjs")],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    mermaid_override = (
        REPO_ROOT / "layouts/_default/_markup/render-codeblock-mermaid.html"
    )
    require(
        mermaid_override.exists(),
        "Hugo-compatible Mermaid code block renderer is missing",
    )
    goat_override = REPO_ROOT / "layouts/_default/_markup/render-codeblock-goat.html"
    require(
        goat_override.exists(),
        "Hugo-compatible Goat code block renderer is missing",
    )
    term_feed_override = REPO_ROOT / "layouts/term.rss.xml"
    require(term_feed_override.exists(), "Hugo-compatible term feed is missing")
    term_feed_text = term_feed_override.read_text()
    require(
        ".Site.Language.Locale" in term_feed_text,
        "term feed does not use the current Hugo language API",
    )
    require(
        ".Site.LanguageCode" not in term_feed_text,
        "term feed still uses the deprecated Hugo language API",
    )

    cdn_data_text = (REPO_ROOT / "assets/data/cdn/jsdelivr.yml").read_text()
    require(
        f"simple-icons@{SIMPLE_ICONS_VERSION}" in cdn_data_text,
        "current Simple Icons release is not configured",
    )
    for relative_path, expected_hash in LUNR_LANGUAGE_HASHES.items():
        actual_hash = hashlib.sha256((REPO_ROOT / relative_path).read_bytes()).hexdigest()
        require(
            actual_hash == expected_hash,
            f"{relative_path} is not from lunr-languages {LUNR_LANGUAGES_VERSION}",
        )


def output_path_for_url(build_dir: Path, source_html: Path, link: str) -> Path | None:
    parsed = urlsplit(link)
    if parsed.scheme or parsed.netloc or link.startswith(("#", "mailto:", "tel:")):
        return None

    decoded_path = unquote(parsed.path)
    if not decoded_path:
        return None
    if decoded_path.startswith("/"):
        relative_url = decoded_path.lstrip("/")
    else:
        source_url = "/" + source_html.relative_to(build_dir).as_posix()
        if source_url.endswith("index.html"):
            source_url = source_url[: -len("index.html")]
        relative_url = posixpath.normpath(
            posixpath.join(posixpath.dirname(source_url), decoded_path)
        ).lstrip("/")

    candidate = build_dir / relative_url
    if decoded_path.endswith("/") or not candidate.suffix:
        candidate = candidate / "index.html"
    return candidate


def verify_internal_links(build_dir: Path) -> None:
    missing: set[tuple[str, str]] = set()
    for html_file in build_dir.rglob("*.html"):
        html_text = html_file.read_text(errors="ignore")
        require(
            re.search(
                r'''(?:href|src|content)=["']http://localhost:1313''', html_text
            )
            is None,
            f"localhost metadata remains in {html_file.relative_to(build_dir)}",
        )
        collector = LinkCollector()
        collector.feed(html_text)
        for link in collector.links:
            candidate = output_path_for_url(build_dir, html_file, link)
            if candidate is not None and not candidate.exists():
                missing.add((html_file.relative_to(build_dir).as_posix(), link))

    if missing:
        details = "\n".join(f"{source}: {link}" for source, link in sorted(missing))
        raise AssertionError(f"broken internal links:\n{details}")


def verify_generated_site() -> None:
    with tempfile.TemporaryDirectory(prefix="cflien-site-") as temporary_dir:
        build_dir = Path(temporary_dir)
        subprocess.run(
            [
                HUGO_BIN,
                "--cleanDestinationDir",
                "--minify",
                "--panicOnWarning",
                "--destination",
                str(build_dir),
                "--noBuildLock",
            ],
            cwd=REPO_ROOT,
            check=True,
            env={
                **os.environ,
                "HUGO_CACHEDIR": str(build_dir / "cache"),
                "HUGO_RESOURCEDIR": str(build_dir / "resources"),
            },
        )

        index_html = (build_dir / "index.html").read_text()
        require(f"<title>{SITE_TITLE}" in index_html, "generated title is not branded")
        require("lunr.min.js" in index_html, "Lunr client script is not loaded")
        require(
            "lunr.stemmer.support.min.js" in index_html,
            "Lunr language stemmer support is not loaded",
        )
        require("lunr.zh.min.js" in index_html, "Lunr Chinese language support is not loaded")
        require(
            f"@fortawesome/fontawesome-free@{FONTAWESOME_VERSION}" in index_html,
            "current Font Awesome release is not loaded",
        )
        require(
            f"typeit@{TYPEIT_VERSION}" in index_html,
            "current TypeIt release is not loaded",
        )
        require(
            any(
                f"emoji-datasource-google@{EMOJI_DATASOURCE_GOOGLE_VERSION}"
                in html_file.read_text(errors="ignore")
                for html_file in build_dir.rglob("*.html")
            ),
            "current Google emoji data release is not loaded",
        )
        generated_html = "\n".join(
            html_file.read_text(errors="ignore")
            for html_file in build_dir.rglob("*.html")
        )
        require("<picture>" in generated_html, "optimized cover picture is not rendered")
        require(
            re.search(r'''type=["']?image/avif''', generated_html) is not None,
            "AVIF cover source is not rendered",
        )
        require(
            re.search(r'''type=["']?image/webp''', generated_html) is not None,
            "WebP cover source is not rendered",
        )
        for post_name, cover_url in post_cover_urls().items():
            require(
                cover_url in generated_html,
                f"{post_name} cover image is not rendered",
            )
            cover_base_url = cover_url.removesuffix(".png")
            for extension in (".avif", ".webp"):
                require(
                    f"{cover_base_url}{extension}" in generated_html,
                    f"{post_name} {extension[1:].upper()} cover is not rendered",
                )
        cover_urls = post_cover_urls()
        newest_cover_url = cover_urls[max(cover_urls, key=post_date)]
        newest_preview_avif = (
            newest_cover_url.removesuffix(".png") + PREVIEW_SUFFIX + ".avif"
        )
        require(
            newest_preview_avif in index_html,
            "home page does not render the preview cover of the newest post",
        )
        require(
            re.search(
                r'<link[^>]*rel=["\']?preload["\']?[^>]*as=["\']?image["\']?[^>]*'
                + re.escape(newest_preview_avif),
                index_html,
            )
            is not None,
            "home page does not preload its LCP cover image",
        )
        headers_path = build_dir / "_headers"
        require(headers_path.is_file(), "Cloudflare Pages _headers file was not generated")
        headers_text = headers_path.read_text()
        require(
            re.search(r"^/\n(?:  .*\n)*  Link: </css/style\.min\.css>; rel=preload; as=style", headers_text, re.M)
            is not None,
            "_headers does not preload the stylesheet for the home page",
        )
        require(
            f"Link: <{newest_preview_avif}>; rel=preload; as=image; type=image/avif" in headers_text,
            "_headers does not preload the newest post preview cover for the home page",
        )
        preloaded_posts = 0
        for html_file in build_dir.rglob("index.html"):
            html_text = html_file.read_text(errors="ignore")
            if "<div class=featured-image>" not in html_text:
                continue
            preloaded_posts += 1
            page_url = html_file.parent.relative_to(build_dir).as_posix()
            page_url = f"/{page_url}/" if page_url != "." else "/"
            preload = re.search(
                r'<link[^>]*rel=["\']?preload["\']?[^>]*as=["\']?image["\']?[^>]*href=["\']?([^"\' >]+\.avif)',
                html_text,
            )
            require(preload is not None, f"{page_url} does not preload its LCP cover image")
            cover_avif = preload.group(1)
            require(
                cover_avif.endswith(".avif") and PREVIEW_SUFFIX not in cover_avif,
                f"{page_url} preloads a preview cover instead of the full cover",
            )
            # Non-ASCII slugs must be present both percent-encoded and decoded.
            for rule_path in {page_url, quote(page_url)}:
                require(
                    re.search(
                        r"^" + re.escape(rule_path) + r"\n(?:  .*\n)*  Link: <" + re.escape(cover_avif)
                        + r">; rel=preload; as=image; type=image/avif",
                        headers_text,
                        re.M,
                    )
                    is not None,
                    f"_headers does not preload the cover of {rule_path}",
                )
        require(
            preloaded_posts == len(cover_urls),
            "not every post page renders a featured image with a preload",
        )
        require("algoliasearch" not in index_html.lower(), "Algolia client is still loaded")
        require(not (build_dir / "en").exists(), "English output remains")
        require(not (build_dir / "1/01/index.html").exists(), "stale /1/01 page remains")
        require(
            not (
                build_dir
                / "2024/12/如何使用-docker-compose-自架-n8n-自動化工作流程平台/index.html"
            ).exists(),
            "stale n8n article URL remains",
        )

        lunr_index_path = build_dir / "index.json"
        require(lunr_index_path.exists(), "Lunr index.json was not generated")
        lunr_index = json.loads(lunr_index_path.read_text())
        require(len(lunr_index) >= 12, "Lunr index does not contain all site content")
        require(
            any("AWS Summit Taipei 2026" in item.get("title", "") for item in lunr_index),
            "Lunr index is missing the latest article",
        )
        verify_internal_links(build_dir)


def main() -> None:
    verify_repository()
    verify_generated_site()
    print("Site verification passed.")


if __name__ == "__main__":
    main()
