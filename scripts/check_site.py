#!/usr/bin/env python3
"""Build the Hugo site and verify its repository and generated output."""

from __future__ import annotations

import json
import os
import posixpath
import re
import subprocess
import tempfile
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
SITE_TITLE = "工程師的摳頂人生"
HUGO_BIN = os.environ.get("CFLIEN_HUGO_BIN", "hugo")
SENSITIVE_SETTING = "ALGOLIA_" + "ADMIN_KEY"


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
