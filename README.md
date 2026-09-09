# CFLien.Me

這是 [CFLien.Me](https://cflien.me/) 的 Hugo 原始碼，使用 LoveIt 主題並由 Cloudflare Pages 發布。

## 本機預覽

先取得網站與主題：

```zsh
git clone --recurse-submodules https://github.com/LienCF/CFLien.Me.git
cd CFLien.Me
hugo server
```

網站與 Cloudflare Pages 統一使用 Hugo Extended 0.164.0。搜尋由 LoveIt 內建的 Lunr 2.3.9 與 lunr-languages 1.20.0 索引提供，不需要 Node.js、Algolia 或其他外部搜尋服務。

## 驗證

```zsh
python3 scripts/check_site.py
```

驗證會在暫存目錄執行乾淨建置，並檢查：

- Hugo warning
- Lunr 搜尋索引
- 內部連結與靜態資源
- 網站標題、語系及 canonical URL
- 已淘汰的部署檔案與敏感設定
- 不應進入版本控制的產生物

## Cloudflare Pages

Cloudflare Pages 專案使用以下設定：

| 設定 | 值 |
| --- | --- |
| Production branch | `main` |
| Build command | `hugo --gc --minify` |
| Build output directory | `public` |
| Environment variable | `HUGO_VERSION=0.164.0` |

`public/` 與 `resources/_gen/` 都是建置產生物，不應提交到 Git。

## pages.dev 導向

`functions/_middleware.js` 是 Cloudflare Pages Function，會把 `cflien-me.pages.dev` 與各次部署的 `*.cflien-me.pages.dev` 以 301 導向 `https://cflien.me`，避免重複內容被索引，也避免掃描器流量被算進網站分析。行為測試在 `scripts/test_pages_dev_redirect.mjs`，`check_site.py` 會一併執行。注意這也會讓分支預覽部署導回正式站。

## 封面圖與 LCP

- 每篇文章的封面放在 `static/images/covers/<slug>.png`，執行 `zsh scripts/optimize_covers.zsh` 會產生 `.avif`、`.webp`，以及首頁摘要卡用的 10:3 裁切版 `-preview.avif`、`-preview.webp`（1300×390）。既有輸出會保留，加 `--force` 才會全部重新編碼。
- 文章頁與首頁最新一篇的封面以 eager 方式載入並在 `<head>` 預載，其餘封面維持 lazyload。
- Hugo 會從 `layouts/home.headers` 產生 Cloudflare Pages 的 `_headers`，為首頁與每篇文章加上 stylesheet 與封面圖的 `Link: rel=preload`，Cloudflare 會據此送出 103 Early Hints。
