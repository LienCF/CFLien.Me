---
title: "Hugo 快速入門指南"
date: 2024-06-26T19:30:00+08:00
draft: false
author: "ChihFeng Lien"
description: "學習如何使用 Hugo 靜態網站產生器建立你的第一個網站"
tags: ["Hugo", "靜態網站", "教學"]
categories: ["documentation"]
---

## 什麼是 Hugo？

Hugo 是一個快速、靈活的靜態網站產生器，使用 Go 語言編寫。它可以將 Markdown 檔案轉換成完整的網站，非常適合建立部落格、文件網站或企業官網。

## 為什麼選擇 Hugo？

- **極快的建置速度**：大型網站也能在幾秒內完成建置
- **簡單易用**：使用 Markdown 撰寫內容
- **豐富的主題**：數百個免費主題可供選擇
- **靈活的部署**：可部署到任何靜態網站託管服務

## 安裝 Hugo

### macOS 安裝

使用 Homebrew 安裝：

```bash
brew install hugo
```

### Windows 安裝

使用 Chocolatey：

```bash
choco install hugo -confirm
```

或者使用 Scoop：

```bash
scoop install hugo
```

### Linux 安裝

在 Ubuntu/Debian 系統上：

```bash
sudo apt install hugo
```

## 建立第一個網站

### 1. 建立新專案

```bash
hugo new site my-website
cd my-website
```

### 2. 新增主題

```bash
git init
git submodule add https://github.com/dillonzq/LoveIt.git themes/LoveIt
```

### 3. 設定主題

在 `config.toml` 檔案中新增：

```toml
baseURL = "https://example.com"
languageCode = "zh-tw"
title = "我的網站"
theme = "LoveIt"
```

### 4. 建立第一篇文章

```bash
hugo new posts/my-first-post.md
```

編輯 `content/posts/my-first-post.md`：

```markdown
---
title: "我的第一篇文章"
date: 2024-06-26T19:30:00+08:00
draft: false
---

這是我的第一篇文章內容！

## 標題

這裡是一些內容...
```

### 5. 本地預覽

```bash
hugo server -D
```

開啟瀏覽器前往 `http://localhost:1313` 查看網站。

### 6. 建置網站

```bash
hugo
```

這會在 `public/` 目錄中生成靜態網站檔案。

## 進階設定

### 自訂設定

編輯 `config.toml` 檔案：

```toml
baseURL = "https://example.com"
languageCode = "zh-tw"
title = "我的技術部落格"
theme = "LoveIt"

[params]
  author = "你的名字"
  description = "這是我的技術部落格"
  
[menu]
  [[menu.main]]
    name = "首頁"
    url = "/"
    weight = 10
  [[menu.main]]
    name = "文章"
    url = "/posts/"
    weight = 20
  [[menu.main]]
    name = "關於"
    url = "/about/"
    weight = 30
```

### 內容組織

建議的目錄結構：

```
content/
├── posts/          # 部落格文章
├── about.md        # 關於頁面
└── contact.md      # 聯絡頁面
```

## 部署

### 部署到 Netlify

1. 將程式碼推送到 GitHub
2. 在 Netlify 連接你的 GitHub 倉庫
3. 設定建置指令：`hugo`
4. 設定發布目錄：`public`

### 部署到 GitHub Pages

在 `.github/workflows/hugo.yml`：

```yaml
name: Deploy Hugo site to Pages

on:
  push:
    branches: ["main"]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'
      - name: Build
        run: hugo --minify
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

## 常用技巧

### 1. 使用 shortcodes

Hugo 提供許多內建的 shortcodes：

```markdown
{{< youtube "你的影片ID" >}}
```

注意：`gist` shortcode 已在 Hugo v0.143.0 中被棄用。如果需要嵌入 GitHub Gist，建議直接使用 HTML 或 JavaScript 嵌入代碼。

### 2. 自訂樣式

在 `assets/css/` 目錄中新增自訂 CSS：

```css
/* custom.css */
.my-custom-style {
    color: #007acc;
}
```

### 3. 多語言支援

在 `config.toml` 中設定：

```toml
defaultContentLanguage = "zh-tw"

[languages]
  [languages.zh-tw]
    title = "我的網站"
    weight = 1
  [languages.en]
    title = "My Website"
    weight = 2
```

## 結語

Hugo 是一個功能強大且易於使用的靜態網站產生器。透過這個快速入門指南，你應該能夠建立並部署你的第一個 Hugo 網站。

想要了解更多進階功能，建議閱讀 [Hugo 官方文件](https://gohugo.io/documentation/)。

---

有任何問題歡迎在留言區討論！ 