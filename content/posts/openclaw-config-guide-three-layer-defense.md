---
title: "OpenClaw 配置指南：打造你的 AI 自動化「三層防線」"
date: 2026-02-03T18:10:00+08:00
draft: false
author: "ChihFeng Lien"
description: "分享如何透過 OpenClaw 的備援機制建立穩健的 AI 自動化環境，包含 Gemini、Anthropic 與 GitHub Copilot 的多層次配置實戰"
tags: ["OpenClaw", "AI", "自動化", "LLM", "DevOps", "SRE"]
categories: ["tech"]
---

## 為什麼我們需要 OpenClaw？

身為 SRE/DevOps 工程師，我們追求的不只是「功能實現」，更是「系統的穩定性」。當你開始依賴 AI 幫你監控郵件、追蹤股價或整理行事曆時，萬一 API 遇到 Quota Limit（額度限制）或 Provider 暫時斷線怎麼辦？

OpenClaw 就是為了解決這個問題而生的。它不僅是一個 AI 執行環境，更強大的是它具備 **Failover（自動備援）** 機制。今天這篇文章將分享我如何配置我的「三層防線」，確保自動化任務永不中斷。

## 核心概念：三層防線

為了分散風險，我們不能把雞蛋放在同一個籃子裡。我的配置邏輯如下：

1.  **第一道防線 (Primary)**：選擇性價比最高、配額最足的模型作為主力。
2.  **第二道防線 (Fallback 1)**：選擇邏輯推理能力更強的模型，處理複雜任務或應付第一道防線的額度用盡。
3.  **第三道防線 (Fallback 2)**：選擇跨平台、不同來源的 Provider，作為最後的連線保證。

## 實戰配置步驟

### 1. 準備 Provider 授權

在開始配置前，確保你已經在 `auth-profiles.json` 中設定好以下 Provider：
- **Google AI Pro**：主戰力來源。
- **Anthropic API**：提供強大的 Claude 4.5 模型。
- **GitHub Copilot**：利用現有的訂閱作為額外保險。

### 2. 修改 openclaw.json

編輯你的 OpenClaw 設定檔，重點在於 `agents.defaults.model` 區塊。以下是我目前使用的滿血配置：

```json
{
  \"agents\": {
    \"defaults\": {
      \"model\": {
        \"primary\": \"google-gemini-cli/gemini-3-flash-preview\",
        \"fallbacks\": [
          \"anthropic/claude-haiku-4-5\",
          \"github-copilot/claude-haiku-4-5\"
        ]
      }
    }
  }
}
```

### 3. 配置解析

- **Primary (Gemini 3 Flash)**：反應速度極快且上下文空間巨大，適合處理日常的高頻率檢查。
- **Fallback 1 (Claude 4.5 Haiku via Anthropic)**：當 Gemini 出現問題時，無縫切換到 Anthropic。4.5 Haiku 的智力水準已經超越上一代的頂級模型，且成本極低。
- **Fallback 2 (Claude 4.5 Haiku via GitHub)**：這是最關鍵的一步。即便 Anthropic 的 API 帳號發生額度或帳單問題，我們仍能透過 GitHub Copilot 的管道調用同款模型。這達到了真正的「來源獨立」。

## 進階技巧：結合 Heartbeat 主動維護

配置好備援後，我還設定了主動的心跳檢查 (`HEARTBEAT.md`)。這讓 OpenClaw 可以定時執行：
- **Outlook 郵件掃描**：偵測 Jenkins 建置失敗或 AWS 警報。
- **投資組合追蹤**：主動回報記憶體族群（如旺宏、群聯）的劇烈震盪。
- **Git 自動提交**：維護工作空間的變更記錄。

## 如何驗證備援是否生效？

你可以嘗試暫時移除 `Primary` 的 API Key，或是故意頻繁調用來觸發額度限制。你會發現 OpenClaw 會安靜地在背景切換到下一個模型，並在日誌中顯示：

```log
[Model Failover] google-gemini-cli/gemini-3-flash-preview failed. 
Rotating to fallback: anthropic/claude-haiku-4-5
```

## 結語

在 2026 年的 AI 時代，**「可用性」就是一切**。透過 OpenClaw 的多層次配置，我們可以建立一個真正可靠的數位助理，讓它在背景守護我們的工作流程，而我們只需專注於高價值的決策。

如果你對 OpenClaw 的安裝或更多進階 Skill 有興趣，歡迎在下方留言討論！

---

*「最好的自動化就是讓你感覺不到它在自動化。」*
