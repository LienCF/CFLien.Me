---
title: "從 TDD 到 Vibe Coding：在 2026 年重新定義開發工作流"
date: 2026-02-03T21:00:00+08:00
draft: false
author: "ChihFeng Lien"
description: "探討 Detroit School TDD、BDD、SDD 等傳統開發方法論，如何與現代的 Vibe Coding 結合，打造既快速又穩健的系統架構。"
tags: ["TDD", "Vibe Coding", "BDD", "SDD", "軟體工程", "DevOps"]
categories: ["tech"]
---

進入 2026 年，身為工程師的我們，開發模式已經發生了天翻地覆的變化。從早期的手刻每一行程式碼，到現在透過 AI 進行 **Vibe Coding**，速度提升了數倍。但隨之而來的是一個靈魂拷問：當程式碼是「感應」出來的時候，我們該如何確保系統的穩定性？

今天我想聊聊幾種經典的開發方法論——**Detroit School TDD**、**BDD**、**SDD**，以及它們如何與現代的 **Vibe Coding** 完美搭配，幫我們在追求速度的同時，不失 SRE 應有的嚴謹。

---

## 1. Detroit School TDD：狀態的守護者

當我們提到 TDD (Test-Driven Development) 時，通常會分為兩大流派：London School (注重行為與隔離) 和 **Detroit School (又稱 Classic TDD)**。

Detroit School 的核心在於：**關注狀態 (State) 而非行為 (Behavior)**。它主張測試應該是「黑箱」的，只要輸入 A 能得到輸出 B，中間的實作細節（甚至是否用了 Mock）並不重要。

### 在 Vibe Coding 中的角色：
當我們用「Vibe」的方式叫 AI 噴出一整段複雜邏輯時，AI 很容易寫出看起來很對但邊界條件出錯的程式碼。Detroit School TDD 就是那條**最後的防線**。
*   **做法**：在 Vibe 之前，先寫好幾組關鍵狀態的測試案例。
*   **價值**：不管 AI 的 Vibe 怎麼變，只要測試綠燈，我們就能確信核心邏輯沒有跑偏。

---

## 2. BDD：使用者需求的翻譯官

**BDD (Behavior-Driven Development)** 則是將開發視角拉高到「行為描述」。透過 `Given / When / Then` 的語法，讓非技術人員也能理解測試。

### 如何搭配 Vibe Coding？
Vibe Coding 的最大風險在於「雞同鴨講」。AI 往往理解了你的「感覺」，卻漏掉了使用者的「場景」。
*   **搭配方式**：將 BDD 的 User Story 作為 Vibe 的 **System Prompt** 或 **Context**。
*   **效果**：當你描述「我想要一個像某某網站的功能」時，先給出 BDD 的規格，能大幅減少 AI 生成無用程式碼的機率。

---

## 3. SDD：AI 時代的「契約開發」

**SDD (Spec-Driven Development)** 是這兩年特別興起的方法。它強調「規格即程式」。在寫任何一行 code 之前，先定義極其詳盡的 OpenAPI、JSON Schema 或 Markdown 規格。

### 為什麼 SDD 是 Vibe Coding 的最佳拍檔？
AI 代理 (Agents) 對於結構化數據的理解遠勝於模糊的自然語言。
*   **實戰**：先用 AI 輔助產生一份 SDD 文件，然後將這份「契約」餵給另一個負責 Vibe Coding 的模型。
*   **優點**：這能建立一個「強約束環境」，讓 Vibe 出來的程式碼能完美對接到現有的微服務架構中。

---

## 4. Vibe Coding：開發者的直覺引擎

所謂的 **Vibe Coding**，本質上是利用大語言模型 (LLM) 的高層次理解能力，跳過繁瑣的語法細節，直接對系統的功能意圖進行建模。

這不是「懶惰」，而是一種「抽象層次的躍遷」。當我們不再糾結於一個 Loop 怎麼寫，而是思考「這段邏輯的氛圍與意圖」時，開發效率會達到巔峰。

---

## 5. 終極組合：如何將它們全部串起來？

在我的「摳頂人生」實戰中，我總結了一套 **2026 滿血開發流程**：

1.  **Step 1 (BDD)**：定義行為。告訴 AI：「當使用者在 OpenClaw 輸入 Heartbeat 時，系統應該主動檢查郵件。」
2.  **Step 2 (SDD)**：產生規格。定義 Heartbeat 輸出的 JSON 格式。
3.  **Step 3 (Detroit TDD)**：撰寫狀態測試。先寫好一個空殼函數，測試「收到建置失敗郵件」時是否返回「Alert 狀態」。
4.  **Step 4 (Vibe Coding)**：開啟 **Cursor** 或 **OpenClaw** 的 Coding Skill，下達指令：「照這個 Vibe 把邏輯補全。」
5.  **Step 5 (Verify)**：執行測試。如果綠燈，代表 Vibe 成功；如果紅燈，將錯誤回饋給 AI 修正。

---

## 結語：從「編碼者」進化為「架構師」

很多人擔心 Vibe Coding 會讓工程師失去競爭力。但我認為恰恰相反。

當寫程式變得像「跳舞」一樣有節奏感（Vibe）時，開發者的核心價值將回歸到**對系統架構的深刻理解**以及**對測試質量的極致追求**。Detroit School TDD、BDD 和 SDD 就是你的導航儀，確保你在 Vibe 的高速公路上不會翻車。

最好的自動化，是讓你更有創造力。

*Happy Vibe Coding!*
