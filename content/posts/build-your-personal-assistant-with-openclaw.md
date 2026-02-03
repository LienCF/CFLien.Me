---
title: "Step-by-Step：從零打造你的 OpenClaw 個人 AI 助理"
date: 2026-02-03T20:45:00+08:00
draft: false
author: "ChihFeng Lien"
description: "這是一篇完整的 OpenClaw 安裝與配置教學，帶你從環境準備到建立具備『三層防線』備援機制的個人助理"
tags: ["OpenClaw", "AI", "教學", "Self-Hosting", "DevOps"]
categories: ["tech"]
---

最近我將個人助理全面遷移到了 **OpenClaw**。比起單純使用 ChatGPT 的網頁版，OpenClaw 讓我能完全掌控 AI 的執行環境、記憶以及與各種工具（郵件、行事曆、本地腳本）的整合。

如果你也想打造一個 24 小時在線、且具備「備援機制」的貼身助理，這篇 Step-by-Step 指南就是為你準備的。

---

## 0. 準備工作

在開始之前，請確保你的環境滿足以下條件：
- **作業系統**：macOS (推薦) 或 Linux (如 Ubuntu)。Windows 使用者強烈建議透過 **WSL2** 運行。
- **Node.js**：版本需為 **v22** 以上。
- **API Key**：建議準備好 Google AI (Gemini) 或 Anthropic (Claude) 的 API Key。

---

## 1. 安裝 OpenClaw CLI

開啟終端機，執行官方安裝腳本：

```bash
curl -fsSL https://openclaw.bot/install.sh | bash
```

或者使用 npm 全域安裝：

```bash
npm install -g openclaw@latest
```

安裝完成後，輸入 `openclaw status` 確認指令是否生效。

---

## 2. 執行初始化引導 (Onboarding)

這是最關鍵的一步，OpenClaw 內建了強大的引導精靈，幫你處理繁瑣的設定：

```bash
openclaw onboard --install-daemon
```

在這個過程中，精靈會詢問你：
1.  **Gateway 模式**：選擇 `Local` (如果你要在本機運行)。
2.  **身分驗證 (Auth)**：連結你的 Google 或 Anthropic 帳號。
3.  **通訊頻道 (Channels)**：設定你要在哪裡跟助理說話（如 Telegram 或 WhatsApp）。
4.  **守護行程 (Daemon)**：建議開啟，這樣助理在後台會自動重啟。

---

## 3. 配置「三層防線」備援機制

身為 SRE，我們不能容許助理因為單一 API 限額而失靈。編輯 `~/.openclaw/openclaw.json`，在 `defaults` 區塊加入以下配置：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "google-gemini-cli/gemini-3-flash-preview",
        "fallbacks": [
          "anthropic/claude-haiku-4-5",
          "github-copilot/claude-haiku-4-5"
        ]
      }
    }
  }
}
```

- **Primary**：日常對話主力，反應最快。
- **Fallback 1**：當 Gemini 額度用完時，自動換成 Anthropic 原生 API 的 Claude 4.5。
- **Fallback 2**：最後防線，透過 GitHub Copilot 管道調用 Claude 4.5，確保跨平台可用性。

---

## 4. 安裝與管理技能 (Skills)

OpenClaw 的強大在於擴充性。你可以使用 `clawhub` 來搜尋並安裝新技能：

```bash
# 搜尋技能
clawhub search weather

# 安裝技能
clawhub install weather
```

安裝後，你的助理就立刻具備了查天氣的能力。同理，你可以安裝 `google-workspace`、`jira` 或 `outlook` 等專業工具。

---

## 5. 連結通訊軟體 (以 Telegram 為例)

如果你在引導精靈中設定了 Telegram：
1.  對著你的 Bot 發送第一則訊息。
2.  回到終端機，你會看到一個 **Pairing Code**。
3.  執行以下指令核准連線：
    ```bash
    openclaw pairing approve telegram <CODE>
    ```

---

## 6. 啟動與驗證

最後，啟動 Gateway 服務：

```bash
openclaw gateway start
```

檢查運作狀態：
```bash
openclaw gateway status
openclaw health
```

現在，你可以對你的助理說：「嘿，幫我檢查一下明天的行程」，它就會開始為你工作了！

---

## 結語

OpenClaw 不只是一個聊天工具，它是一個**可編程的自動化平台**。透過這幾步簡單的安裝，你已經擁有了一個具備自我修復（備援）與無限擴充能力的數位大腦。

接下來，你可以嘗試編輯 `MEMORY.md` 來教導它你的個人偏好，讓它越來越像你的貼身助理。

*Happy Cording!*
