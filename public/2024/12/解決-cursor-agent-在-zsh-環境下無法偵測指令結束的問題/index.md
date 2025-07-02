# 解決 Cursor Agent 在 Zsh 環境下無法偵測指令結束的問題


## 問題描述

當你將 Cursor 的整合終端切換為 zsh，特別是搭配 Oh My Zsh 或 Powerlevel10k 主題後，可能會遇到以下困擾：

1. **Agent 執行指令後卡住不動**：Cursor 無法自動偵測命令執行完成
2. **需要手動點擊 Skip**：每次都要人工介入才能繼續
3. **出現 `q` 指令錯誤**：Skip 後會看到 `zsh: command not found: q` 的錯誤訊息

這個問題不僅影響工作流程的順暢度，也讓原本應該自動化的 AI Assistant 體驗大打折扣。

## 問題根本原因分析

### 1. Prompt 解析失敗

Cursor Agent 在執行 `run_terminal_cmd` 時，會透過解析 shell prompt 的字串來判斷命令是否結束。然而：

- **zsh 的複雜 prompt**：Oh My Zsh 和 Powerlevel10k 產生的 prompt 包含大量彩色字元、特殊符號和動態內容
- **匹配模式無法識別**：Cursor 內建的 prompt 匹配規則無法正確識別這些複雜的 prompt 格式
- **結果持續等待**：系統誤判命令仍在執行中，因此一直等待結束信號

### 2. Pager 干擾機制

Cursor 為了處理長輸出，會將命令包在分頁器（pager）流程中：

```bash
# Cursor 內部執行方式類似
command | less
```

當偵測不到結束信號時，Cursor 認為可能卡在分頁器中。

### 3. Skip 操作的副作用

當使用者點擊 Skip 時，Cursor 會：

1. **發送 `q` 字元**：嘗試退出 pager（`less` 的標準退出鍵）
2. **直接執行為命令**：但此時已脫離 pager 環境，`q` 被當作一般指令
3. **產生錯誤訊息**：zsh 找不到名為 `q` 的程式，輸出錯誤

## 解決方案

### 方法一：針對 Cursor Agent 停用 Pager

最直接的解決方案是在 `.zshrc` 中偵測 Cursor Agent 環境，並針對性地調整設定：

```bash
# ~/.zshrc

# Detect Cursor Agent environment and disable pager
if [[ -n $CURSOR_TRACE_ID ]]; then
  export PAGER=cat
  export LESS='-RF'
fi

# Your existing Oh My Zsh configuration
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="powerlevel10k/powerlevel10k"
source $ZSH/oh-my-zsh.sh

# Load Powerlevel10k configuration
[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh
```

**重要說明**：
- 不要在 `if` 區塊後加上 `return`，這會導致主題無法載入
- 僅修改 pager 相關設定，保留完整的 zsh 功能

### 方法二：建立 Cursor 專用的簡化設定檔

如果你想要更精確的控制，可以建立一個專門的設定檔：

```bash
# ~/.zshrc

if [[ -n $CURSOR_TRACE_ID ]]; then
  # Cursor Agent specific settings
  export PAGER=cat
  export LESS='-RF'
  export MANPAGER=cat
  
  # Use minimal prompt for better detection
  export PS1='%n@%m:%~$ '
  
  # Skip complex theme loading for agent
  export CURSOR_AGENT_MODE=true
fi

# Load full configuration only if not in agent mode
if [[ -z $CURSOR_AGENT_MODE ]]; then
  export ZSH="$HOME/.oh-my-zsh"
  ZSH_THEME="powerlevel10k/powerlevel10k"
  source $ZSH/oh-my-zsh.sh
  [[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh
else
  # Minimal setup for agent mode
  autoload -U compinit
  compinit
fi
```

### 方法三：使用條件式主題載入（推薦）

這個方法既能解決 Agent 問題，又能在一般終端中保留完整的主題體驗：

```bash
# ~/.zshrc

# Always load basic zsh functionality
autoload -Uz compinit
compinit

# Configure pager for Cursor Agent
if [[ -n $CURSOR_TRACE_ID ]]; then
  export PAGER=cat
  export LESS='-RF'
  export MANPAGER=cat
fi

# Load Oh My Zsh and themes
export ZSH="$HOME/.oh-my-zsh"

# Use simplified theme in Cursor Agent mode
if [[ -n $CURSOR_TRACE_ID ]]; then
  ZSH_THEME="robbyrussell"  # Simple theme for better compatibility
else
  ZSH_THEME="powerlevel10k/powerlevel10k"  # Full theme for interactive use
fi

source $ZSH/oh-my-zsh.sh

# Load Powerlevel10k only in interactive mode
if [[ -z $CURSOR_TRACE_ID && -f ~/.p10k.zsh ]]; then
  source ~/.p10k.zsh
fi
```

## 環境變數說明

### CURSOR_TRACE_ID

這是 Cursor Agent 執行時設定的環境變數，可以用來偵測是否在 Agent 模式下執行：

```bash
# Check if running in Cursor Agent mode
echo $CURSOR_TRACE_ID
```

### PAGER 設定選項

```bash
# Option 1: Use cat (no paging)
export PAGER=cat

# Option 2: Use less with specific flags
export PAGER=less
export LESS='-RF'  # -R: raw control chars, -F: quit if one screen

# Option 3: Disable pager completely
unset PAGER
```

## 驗證解決方案

### 1. 測試 Agent 指令執行

重新啟動 Cursor 後，測試 Agent 執行簡單指令：

```bash
ls -la
```

應該能看到：
- ✅ 指令正常執行完成
- ✅ Cursor 自動偵測到執行結束
- ✅ 不需要手動 Skip
- ✅ 沒有 `command not found: q` 錯誤

### 2. 確認終端主題正常

在 Cursor 中手動開啟新的終端分頁：

```bash
# Should show your configured theme
echo $ZSH_THEME

# Check if Powerlevel10k is loaded (if using)
p10k version
```

### 3. 測試長輸出處理

```bash
# Test with long output
find /usr -name "*.dylib" 2>/dev/null
```

應該能正常顯示而不會卡在分頁器中。

## 進階調整

### 自訂 Cursor Agent 偵測

如果 `CURSOR_TRACE_ID` 偵測不穩定，可以使用其他方法：

```bash
# ~/.zshrc

# Multiple detection methods
is_cursor_agent() {
  [[ -n $CURSOR_TRACE_ID ]] || 
  [[ $TERM_PROGRAM == "cursor" && -n $VSCODE_INJECTION ]] ||
  [[ -n $CURSOR_USER_ID ]]
}

if is_cursor_agent; then
  export PAGER=cat
  export LESS='-RF'
fi
```

### 日誌記錄調試

添加日誌來追蹤設定載入情況：

```bash
# ~/.zshrc

# Debug logging
CURSOR_DEBUG_LOG="$HOME/.cursor_zsh_debug.log"

log_debug() {
  echo "[$(date)] $1" >> "$CURSOR_DEBUG_LOG"
}

if [[ -n $CURSOR_TRACE_ID ]]; then
  log_debug "Cursor Agent detected: $CURSOR_TRACE_ID"
  export PAGER=cat
  log_debug "PAGER set to cat"
fi
```

## 常見問題排解

### Q: 設定後仍然卡住怎麼辦？

**A**: 檢查以下項目：

1. 確認 `.zshrc` 語法正確：
   ```bash
   zsh -n ~/.zshrc
   ```

2. 檢查環境變數是否正確設定：
   ```bash
   env | grep -E "(PAGER|LESS|CURSOR)"
   ```

3. 重新啟動 Cursor 確保設定生效

### Q: 主題沒有載入怎麼辦？

**A**: 確保沒有在設定區塊後使用 `return`：

```bash
# ❌ Wrong - this will skip theme loading
if [[ -n $CURSOR_TRACE_ID ]]; then
  export PAGER=cat
  return  # This breaks theme loading
fi

# ✅ Correct - theme will load normally
if [[ -n $CURSOR_TRACE_ID ]]; then
  export PAGER=cat
fi
```

### Q: 其他編輯器會受影響嗎？

**A**: 不會。設定僅在偵測到 `CURSOR_TRACE_ID` 時生效，不會影響其他編輯器或終端應用程式。

## 總結

透過在 `.zshrc` 中針對 Cursor Agent 環境進行條件式設定，我們可以：

1. **解決指令偵測問題**：避免 Agent 卡住等待
2. **消除錯誤訊息**：不再出現 `command not found: q`
3. **保留完整功能**：在一般終端中仍享有完整的 zsh 主題體驗
4. **提升工作效率**：讓 AI Assistant 功能重新順暢運作

這個解決方案的核心是理解 Cursor Agent 的運作機制，並針對性地調整環境設定，而非完全捨棄 zsh 的強大功能。記住，好的開發環境設定應該是既實用又不犧牲功能性的平衡。

## 參考資源

- [Cursor Agent Terminal Commands Issue](https://forum.cursor.com/t/bug-ai-assistant-terminal-commands-never-auto-complete/101844)
- [Zsh Command Not Found: q](https://forum.cursor.com/t/zsh-command-not-found-q/101502)
- [Oh My Zsh Configuration Guide](https://github.com/ohmyzsh/ohmyzsh)
- [Powerlevel10k Documentation](https://github.com/romkatv/powerlevel10k) 
