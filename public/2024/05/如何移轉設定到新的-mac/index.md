# 如何移轉設定到新的 MAC


## 前言

更換新的工作機總是一件令人興奮的事，但伴隨而來的是繁瑣的環境設定。為了讓轉移過程更順利，我將在本篇文章中記錄如何系統性地備份、移轉，並還原我的個人化設定，特別是針對開發者常用的工具。

## 使用 Homebrew 進行套件管理

[Homebrew](https://brew.sh/) 是 macOS 上不可或缺的套件管理器。透過 Brewfile，我們可以輕鬆地將所有已安裝的套件列表匯出，並在新機器上快速安裝回來。

### 備份已安裝的套件

在舊的 Mac 上執行以下指令，會產生一個名為 `Brewfile` 的檔案，裡面包含了所有透過 Homebrew 安裝的 Formulae、Casks 和來自 Mac App Store 的應用程式。

```bash
brew bundle dump
```

### 在新 Mac 上還原套件

將 `Brewfile` 檔案複製到新的 Mac 上，然後在同一個目錄下執行：

```bash
brew bundle install
```

Homebrew 會自動安裝檔案中列出的所有項目。


## 設定免密碼 sudo

有時候在開發環境下，頻繁輸入 sudo 密碼會很麻煩。你可以透過以下步驟，讓自己的帳號在執行 sudo 指令時不需要輸入密碼：

1. 在終端機輸入以下指令來編輯 sudoers 檔案（建議使用 `visudo` 來避免語法錯誤）：

```bash
    sudo visudo
```

2. 在打開的編輯器中，於檔案最後加上以下這一行（請將 `your_username` 替換成你的 macOS 使用者名稱）：

```
your_username ALL=(ALL) NOPASSWD: ALL
```

> 例如，如果你的使用者名稱是 `alice`，就寫成：
> 
> ```
> alice ALL=(ALL) NOPASSWD: ALL
> ```

3. 儲存並關閉檔案。

> ⚠️ **注意安全性**：這樣做會讓你的帳號執行任何 sudo 指令時都不需要密碼，請務必確認你的電腦安全，且不要在公用或多人共用的電腦上這樣設定。

## 啟用遠端連線功能

macOS 內建了 SSH 和遠端桌面功能，讓你可以從其他裝置遠端存取你的 Mac。以下是啟用這些功能的步驟：

### 啟用 SSH 遠端連線

1. 開啟「系統設定」(System Settings)
2. 點選「一般」(General) →「分享」(Sharing)
3. 找到並開啟「遠端登入」(Remote Login)

## 備份與還原 VS Code 設定

[Visual Studio Code](https://code.visualstudio.com/) 是我主要的程式碼編輯器。它的設定、快捷鍵、以及已安裝的擴充功能都可以透過內建的「Settings Sync」功能進行同步。

1. **開啟 Settings Sync**：在 VS Code 的設定中，搜尋 "Settings Sync" 並啟用它。
2. **登入帳號**：你可以選擇使用 Microsoft 或 GitHub 帳號登入。
3. **在新 Mac 上登入**：在新機器的 VS Code 上登入同一個帳號，設定就會自動同步下來。

## 同步 Shell 設定

我的 Shell 環境 (Zsh) 有許多客製化的別名 (alias) 和函式。這些設定通常存放在 `~/.zshrc` 或 `~/.bash_profile` 檔案中。我推薦使用一個 Git repository 來管理這些 "dotfiles"。

1. 建立一個私有的 GitHub repository。
2. 將你的 `~/.zshrc`, `~/.gitconfig` 等設定檔放進去。
3. 在新機器上 clone 這個 repository，然後用 symbolic links 將它們連結到 home 目錄下。

這樣不僅方便移轉，也能做到版本控制。

## 其他應用程式設定

對於沒有內建同步功能的應用程式，大部分的設定檔會存放在 `~/Library/Application Support/` 或 `~/Library/Preferences/` 路徑下。你可以手動備份這些資料夾，但建議只針對你真正需要的應用程式進行操作，避免複製到不必要的系統檔案。

希望這份筆記能幫助到需要移轉 Mac 設定的你！

