# 如何在 Cursor 中將預設終端由 PowerShell 變更為 Zsh


## 前言

Cursor 是一款基於 VS Code 的 AI 程式編輯器，因此許多 VS Code 的設定方式在 Cursor 中同樣適用。預設情況下，Cursor 會根據作業系統選擇預設的終端 Shell。在 macOS 上，雖然系統預設已經是 Zsh，但有時 Cursor 可能會選擇其他 Shell 如 PowerShell 或 Bash。本文將教你如何手動設定 Zsh 為 Cursor 的預設整合終端。

## 為什麼選擇 Zsh？

Zsh (Z Shell) 是一個功能強大的 Shell，具有以下優點：

- **強大的自動補全功能**：比 Bash 更智慧的 Tab 補全
- **豐富的主題支援**：如 Oh My Zsh 框架提供的美觀主題
- **更好的歷史記錄管理**：支援歷史記錄搜尋和共享
- **插件生態系統**：豐富的插件可擴展功能
- **macOS 原生支援**：自 macOS Catalina 起為系統預設 Shell

## 方法一：使用命令面板設定

這是最簡單直接的方法：

### 步驟

1. **開啟命令面板**
   - 按下 `⌘Cmd` + `⇧Shift` + `P`（macOS）
   - 或按下 `Ctrl` + `Shift` + `P`（Windows/Linux）

2. **選擇預設終端設定檔**
   - 在命令面板中輸入 `Terminal: Select Default Profile`
   - 選擇該選項

3. **選擇 Zsh**
   - 在出現的下拉清單中點選 **zsh**
   - 如果看不到 zsh 選項，表示可能需要先安裝或設定 zsh

4. **重啟終端**
   - 關閉所有已開啟的終端分頁
   - 使用 `⌘Cmd` + `` ` `` 開啟新的終端
   - 新終端將會使用 Zsh

## 方法二：編輯設定檔

對於喜歡手動設定的使用者，可以直接編輯 Cursor 的設定檔：

### 步驟

1. **開啟設定檔**
   - 按下 `⌘Cmd` + `⇧Shift` + `P` 開啟命令面板
   - 輸入 `Preferences: Open Settings (JSON)` 並選擇

2. **新增 macOS 設定**
   
   在 JSON 檔中新增或修改以下設定：

   ```json
   {
     "terminal.integrated.defaultProfile.osx": "zsh"
   }
   ```

3. **（選用）自訂 Zsh 設定檔**
   
   如果需要指定特定的 Zsh 路徑或啟動參數：

   ```json
   {
     "terminal.integrated.defaultProfile.osx": "zsh",
     "terminal.integrated.profiles.osx": {
       "zsh": {
         "path": "/bin/zsh",
         "args": ["-l"]
       }
     }
   }
   ```

4. **儲存並重啟**
   - 按下 `⌘Cmd` + `S` 儲存設定檔
   - 關閉現有終端分頁並開啟新的終端

## 驗證設定

設定完成後，可以透過以下方式驗證：

1. **檢查 Shell 類型**
   ```bash
   echo $SHELL
   ```
   應該顯示 `/bin/zsh` 或類似路徑

2. **檢查 Zsh 版本**
   ```bash
   zsh --version
   ```

3. **查看終端標題**
   - 新開的終端分頁標題應該顯示 "zsh"

## 常見問題排解

### 問題 1：找不到 zsh 選項

**解決方案：**
```bash
# 確認 zsh 是否已安裝
which zsh

# macOS 使用 Homebrew 安裝
brew install zsh

# 將 zsh 加入允許的 Shell 清單
echo $(which zsh) | sudo tee -a /etc/shells

# 設定為預設 Shell
chsh -s $(which zsh)
```

### 問題 2：Zsh 設定檔案問題

**解決方案：**
確保 `~/.zshrc` 檔案存在且配置正確：

```bash
# 建立基本的 .zshrc 檔案
touch ~/.zshrc

# 新增基本設定
echo 'export PATH=$HOME/bin:/usr/local/bin:$PATH' >> ~/.zshrc
```

### 問題 3：終端啟動緩慢

**解決方案：**
檢查 `~/.zshrc` 中是否有耗時的設定：

```bash
# 使用時間測量工具檢查啟動時間
time zsh -i -c exit

# 暫時停用 Oh My Zsh（如果有安裝）
mv ~/.oh-my-zsh ~/.oh-my-zsh.bak
```

## 進階設定

### 整合 Oh My Zsh

如果你使用 Oh My Zsh 框架：

```bash
# 安裝 Oh My Zsh
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 設定主題（編輯 ~/.zshrc）
ZSH_THEME="agnoster"  # 或其他喜歡的主題
```

### 自訂 Cursor 終端外觀

在 Cursor 設定中新增：

```json
{
  "terminal.integrated.fontSize": 14,
  "terminal.integrated.fontFamily": "MesloLGS NF",
  "terminal.integrated.cursorStyle": "line",
  "terminal.integrated.cursorBlinking": true
}
  ```

## 常見問題與後續設定

### Cursor Agent 指令偵測問題

在設定 zsh 為預設終端後，你可能會遇到 Cursor Agent 執行指令時無法自動偵測指令結束的問題，需要手動點擊 Skip 且出現 `command not found: q` 錯誤。

這是因為 zsh 的複雜 prompt（特別是 Oh My Zsh 或 Powerlevel10k 主題）會影響 Cursor 的指令結束偵測機制。

**快速解決方法**：在 `~/.zshrc` 中加入以下設定：

```bash
# Detect Cursor Agent environment and disable pager
if [[ -n $CURSOR_TRACE_ID ]]; then
  export PAGER=cat
  export LESS='-RF'
fi
```

詳細的問題分析和完整解決方案，請參考相關文章：[解決 Cursor Agent 在 Zsh 環境下無法偵測指令結束的問題](cursor-zsh-agent-command-detection-issue.md)

## 參考資源

- [Cursor 官方文件](https://cursor.sh/)
- [Oh My Zsh 官網](https://ohmyz.sh/)
- [Zsh 官方文件](https://zsh.sourceforge.io/)
- [VS Code Terminal 設定指南](https://code.visualstudio.com/docs/terminal/profiles) 
