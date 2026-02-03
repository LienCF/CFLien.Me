---
title: "深度探討 2026 開發範式：當 Detroit School TDD、BDD、SDD 遇上 Vibe Coding"
date: 2026-02-03T19:10:00+08:00
draft: false
author: "ChihFeng Lien"
description: "這是一篇深入剖析傳統軟體工程嚴謹的方法論如何成為現代 AI 輔助開發（Vibe Coding）的穩壓器。我們將從測試、行為、規格三個維度，重新定義 SRE 等級的開發流程。"
tags: ["TDD", "Vibe Coding", "BDD", "SDD", "軟體架構", "DevOps", "SRE"]
categories: ["tech"]
---

在 2026 年的今天，開發者的角色正經歷一場前所未有的「身份危機」。隨著 Vibe Coding 的興起，程式碼的產出速度已經不再是瓶頸。然而，身為一名長期浸淫在 SRE 與 DevOps 領域的工程師，我觀察到一個危險的趨勢：開發者正逐漸喪失對程式碼邏輯的掌控權。

當我們僅憑「感覺 (Vibe)」來引導 AI 生成數千行程式碼時，我們實際上是在建立一座沒有地基的海市蜃樓。為了讓 Vibe Coding 從「實驗室特技」轉化為「生產環境基準」，我們必須召回那些被遺忘的經典方法論：Detroit School TDD、BDD 與 SDD。

這篇文章將深入探討，這三種傳統的嚴謹框架，如何成為現代 AI 開發中的「穩壓器」與「導航系統」。

---

## 一、 Detroit School TDD：AI 生成內容的黑箱驗證器

在 TDD (Test-Driven Development) 的歷史中，一直存在著兩大流派的爭執：London School (Mockist) 與 Detroit School (Classicist)。

### 1. 為什麼不是 London School？
London School 強調「行為測試」，依賴大量的 Mock 物件來隔離相依性。在手刻代碼的年代，這能幫你釐清物件間的互動。但在 AI 時代，Mock 變成了災難。AI 常常會為了滿足 Mock 的設定而寫出極其脆弱、與現實脫節的「特供版邏輯」。

### 2. Detroit School 的回歸
Detroit School 主張「狀態測試」。它不關心你內部是怎麼呼叫資料庫的，它只關心：當我輸入一筆訂單，最後庫存有沒有扣除。

在 Vibe Coding 中的應用：
當我下達「幫我寫一個處理退款的邏輯」這個 Vibe 指令前，我會先要求 AI（或我自己動手）寫下幾組測試：
*   Test 1: 正常餘額退款 -> 預期餘額增加，訂單狀態變更。
*   Test 2: 重複退款請求 -> 預期報錯，不應重複扣款。

這就是所謂的 「測試圍欄 (Test Fence)」。AI 在圍欄內怎麼 Vibe、怎麼重構都不重要，只要測試綠燈，我們就擁有了 SRE 等級的信心。

---

## 二、 BDD：將「意圖」轉化為精準的 Prompt

BDD (Behavior-Driven Development) 的精髓在於 Ubiquitous Language (通用語言)。它要求我們用 Given (前提), When (操作), Then (結果) 來描述系統。

### 1. 解決 Vibe Coding 的模糊性
Vibe Coding 最常被詬病的就是「指令模糊」。一句「幫我做個漂亮的首頁」對不同模型的定義完全不同。

### 2. BDD 作為「高品質 Prompt 模板」
透過 BDD 框架，我們可以將意圖結構化：
*   Given: 使用者已登入且具備 VIP 權限。
*   When: 點擊「領取優惠」按鈕時。
*   Then: 系統應檢查其領取紀錄，若未領取則派發序號，並發送 Telegram 通知。

這不是在寫 Code，這是在定義「Vibe 的邊界」。當 AI 拿到這種結構的文章時，它生成的程式碼精準度會從 60% 提升到 95% 以上。

---

## 三、 SDD：在 AI 代理間建立「契約精神」

SDD (Spec-Driven Development) 是現代複雜系統的救星。它強調：規格書即是真理 (Source of Truth)。

### 1. 消除「溝通損耗」
在傳統團隊中，規格書寫完就過時了。但在 2026 年，我們有 MCP (Model Context Protocol) 與各種 AI 代理。助理（如 OpenClaw）可以直接讀取 OpenAPI 或 JSON Schema。

### 2. 實戰流程：規格先行
當我今天要開發一個新的「投資追蹤 Skill」時，我的流程如下：
1.  定義 Schema：使用 JSON Schema 定義「股價數據」的標準格式（包含時間、代號、開高低收）。
2.  強制約束：告訴 Vibe Coding 模型：「你寫出的所有輸出，必須通過這份 Schema 的驗證。」
3.  合約測試：使用自動化工具檢查 AI 產出的 API 是否符合原始規格。

這確保了雖然程式碼是 AI 寫的，但它的「形狀」是完全受控的。

---

## 四、 Vibe Coding：工程師的「第二大腦」

在定義好 TDD、BDD 與 SDD 後，我們終於可以聊聊 Vibe Coding 了。

Vibe Coding 代表的是一種 「流態開發 (Flow-State Development)」。它讓我們擺脫了編譯錯誤、語法細節等低層次的認知負荷。

*   它的強項：快速原型設計、模板代碼生成、邏輯重構建議。
*   它的弱點：對邊界條件的忽視、對系統穩定性的盲目樂觀。

SRE 的觀點：Vibe Coding 就像是一台超高性能的跑車引擎，而 TDD/BDD/SDD 則是底盤與煞車系統。沒有底盤，引擎只會帶著你衝下懸崖。

---

## 五、 2026 滿血開發工作流：案例研究

假設我們要開發一個 「自動化備援切換器」（就像我們今天在 OpenClaw 做的）。

### 第一步：BDD 定義場景
我們寫下：「若主力模型 (Gemini) 報錯，系統應在 3 秒內自動嘗試第一備援 (Claude)，並發送警報通知給 Alex。」

### 第二步：SDD 定義數據結構
定義警報物件的 JSON 格式：{ timestamp, source_error, rotated_to, status }。

### 第三步：Detroit TDD 寫下測試
```python
def test_failover_logic():
    # 模擬 Gemini 斷線狀態
    with mock_gemini_failure():
        result = trigger_request()
        # 驗證最終狀態
        assert result.status == "recovered"
        assert result.rotated_to == "anthropic/claude-haiku-4-5"
```

### 第四步：Vibe Coding 噴出實實作
對 AI 說：「參考上面的 BDD 場景與 TDD 測試，用你覺得最優雅、最非同步的方式把 FailoverHandler Vibe 出來。」

### 第五步：持續監控 (The SRE Way)
利用 ActivityWatch 觀察這段 Code 的執行效率，並將日誌回饋給 AI 進行下一輪的 Vibe 優化。

---

## 結語：我們正在進步，還是退步？

有人問我：當 AI 能寫出 90% 的程式碼時，工程師還有價值嗎？

我的回答始終如一：在 Vibe Coding 時代，工程師的價值在於「定義問題」與「保證正確」。

如果你只會寫 Code，你會被取代；但如果你學會利用 Detroit School TDD 來守護狀態、利用 BDD 來對齊行為、利用 SDD 來鞏固規格，那麼 Vibe Coding 對你來說就不是威脅，而是讓你從「碼農」進化為「系統建築師」的終極階梯。

科技進步的本質，不是為了取代人類的思考，而是為了釋放人類的創造力。

Keep Coding, Keep Vibing.

---

如果你喜歡這篇文章，歡迎轉發給正在與 AI 磨合的開發者夥伴們！
