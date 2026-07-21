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
