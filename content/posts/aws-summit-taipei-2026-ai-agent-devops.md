---
title: "AWS Summit Taipei 2026 觀察：AI Agent 正在如何改變 DevOps"
date: 2026-07-17T15:20:00+08:00
draft: false
author: "ChihFeng Lien"
description: "整理 AWS Summit Taipei 2026 的 Keynote 與 Workshop 重點，從 Amazon Quick、Kiro CLI、EKS Auto Mode 到 AWS DevOps Agent，分析 AI Agent 對 DevOps、平台工程與維運工作的實際影響。"
url: "/2026/07/aws-summit-taipei-2026-ai-agent-devops/"
tags: ["AWS", "AWS Summit", "AI Agent", "DevOps", "SRE", "Kubernetes", "Amazon EKS", "Kiro"]
categories: ["tech"]
---

這次 AWS Summit Taipei 2026，我最在意的不是又多了哪些模型或產品，而是 **AI Agent 開始真正走進軟體交付與維運流程之後，DevOps 的工作會怎麼變**。

兩天的內容從 Amazon Quick、Kiro CLI、Amazon EKS Auto Mode、AWS DevOps Agent，一路談到 Amazon Bedrock AgentCore、AWS Transform、Codex 與 Claude。看起來各自處理不同問題，放在一起卻指向同一件事：模型能力已經不是唯一瓶頸。要讓 Agent 進入正式工作，還需要正確的脈絡、受控的工具權限、可觀測的執行環境、可驗證的結果，以及清楚的人機責任邊界。

這也是我認為 DevOps 接下來最重要的轉變。重點不只是會不會用更多 AI 工具，而是能不能把交付與維運流程設計成 Agent 看得懂、做得到、查得到證據，出錯時也停得下來、回得去。

## 我先講結論

- AI Agent 的價值不在多一個聊天視窗，而在能否帶著工作脈絡使用工具，完成一段可驗證的流程。
- Coding 變快之後，瓶頸會往 code review、security、release 與 operations 移動。只加速寫程式，通常只是把問題推到下一站。
- Incident investigation 很適合先導入 Agent，因為它能整合 topology、metrics、logs、events 與 deployment context。但調查、建議與修復應該維持不同權限層級。
- DevOps 不會因為 Agent 而消失。相反地，權限、平台介面、可觀測性、供應鏈、變更證據與回復能力會變得更重要。
- 自主程度不該一開始就拉滿。比較務實的路線是從唯讀調查開始，再逐步開放低風險、可回復且可觀測的寫入動作。

## Keynote：Agent 不是功能，而是一套工作系統

### Day 1：從寫程式走向完整交付閉環

第一天最清楚的訊息，是企業已經不太需要繼續辯論「要不要用 AI」，真正需要回答的是：要把 AI 放在哪些高價值工作上，以及怎麼控制風險。

如果每次任務都能取得需求、規格、文件、組織關係、歷史決策與回饋，Agent 才有機會累積脈絡，讓結果逐步改善。反過來說，如果人還是要在 email、文件、ticket、程式碼與監控系統之間手動搬資料，AI 再聰明也只是更快的搜尋與文字產生工具。

軟體交付被拆成三個連續階段：

1. **Write it right**：用需求、規格、技術標準與測試脈絡約束程式碼產生，不只追求寫得快。
2. **Ship it fast**：讓 review、security、test、release 與 deployment 跟上開發速度。
3. **Keep it modern**：把舊系統分析、升級與技術債處理變成持續能力，而不是幾年一次的大型專案。

Kiro、AWS DevOps Agent 與 AWS Transform 分別落在這條閉環的不同位置。這個組合提醒我一件很實際的事：當 coding agent 大幅提高程式碼產量，原本藏在後段的瓶頸會立刻浮出來。測試環境不穩、審查排隊、權限混亂、發布流程脆弱，最後都會比寫程式本身更慢。

Agent 要進正式環境，也需要三層基礎：

- **安全與治理**：決定可以讀什麼、做什麼，哪些動作一定要人工核准。
- **執行基礎**：提供 runtime、memory、identity、tool integration、observability 與穩定的 orchestration loop。
- **資料與脈絡**：把企業文件、結構化資料、歷史紀錄與組織知識放進同一個決策環境。

Amazon Bedrock AgentCore 處理的是 Agent 生產化所需的 runtime、memory、identity、policy 與 observability。Codex 則呈現另一個角度：軟體工程正在從 autocomplete、人機協作，走向把較完整的任務交給 Agent 執行。這時候真正值得衡量的，不是產生多少行程式碼，而是完成多少經過測試、審查與驗證的工作。

### Day 2：可信任的 AI，底下仍然是可靠的基礎設施

第二天把焦點拉回資料在地、低延遲、韌性與企業信任。AWS Asia Pacific (Taipei) Region 提供三個 Availability Zone，讓台灣的 workload 有更好的在地架構條件，但 Region 與多 AZ 只是設計材料，不會讓系統自動符合監管要求，也不會自動變成高可用。

Nasdaq 的案例讓這件事更具體。當市場逐步朝接近全天候運作前進，維護窗口會縮小，跨時區 on-call、無停機變更、容量管理與回復能力都會變得更嚴格。這些不是模型問題，而是很典型的 SRE 與平台工程問題。

KBS 的應用則顯示，AI 原生流程不是把 AI 塞進現有步驟，而是重新設計內容擷取、辨識、分析、製作、直播與分發方式。對軟體交付來說也是如此。真正的改變不只是讓某個步驟快一點，而是重新思考需求、開發、驗證、部署與營運之間怎麼傳遞脈絡。

我把第二天的核心理解成一句話：**可信任的 AI，不只取決於模型，也取決於資料、權限、基礎設施、監督與營運控制能不能一起成立。**

## Workshop：從知識工作一路做到 Kubernetes 維運

### Amazon Quick：把日常判斷變成可重複的流程

Amazon Quick 的實作不是單純做 email 摘要，而是把 email、通訊、行事曆、文件、排程與個人判斷串成一條工作流程。

實際操作涵蓋：

- 連接 email、通訊與行事曆，設定工具使用前的授權偏好。
- 用 Activity Feed 集中未讀資訊、分類內容、產生摘要與建議動作。
- 建立 Scheduled task，定期整理信件與待辦事項。
- 把客戶、專案、活動優先順序等個人判斷寫成 Agent 可讀的規則。
- 建立專用 Agent，同時參考 email、行事曆、團隊資料與個人規則，提出排序與下一步建議。
- 使用 Browser Automation 操作網頁流程，或讓 Deep analysis 先提出研究計畫，再進行較長時間的資料蒐集與分析。

這裡最值得帶回 DevOps 的，不是信件分類，而是 **把隱性判斷外顯化**。Incident priority、change risk、service tier、escalation path、maintenance policy，很多時候都存在資深工程師腦中。Agent 要可靠地協助工作，這些規則必須變成有版本、有 owner、有適用範圍，也能定期覆核的 operational context。

如果規則只藏在某個人的 prompt 裡，它不會變成團隊能力，也很難治理。

### Kiro CLI、EKS Auto Mode 與 AWS DevOps Agent：一條完整的實作路徑

另一個 Workshop 把開發、部署、擴縮、可觀測性與故障調查串在一起。

Kiro CLI 先透過幾個控制面建立工作邊界：

- **Steering** 保存專案、架構與部署規則。
- **Skills** 封裝可以重複使用的工作方法。
- **MCP Servers** 提供 AWS、EKS、文件與外部資料的工具介面。
- **Permissions 與 trust** 決定哪些工具可以自動執行，哪些動作必須逐次核准。

接著由 Kiro CLI 建立 React 前端，完成 build 與 test，再建立 Docker image、推送到 Amazon ECR、產生 Kubernetes resources，最後部署到 EKS Auto Mode。應用程式透過 Application Load Balancer 對外服務，並加入 Horizontal Pod Autoscaler 與 CloudWatch Container Insights。

這條流程證明 Coding Agent 已經可以跨越程式碼、本機工具、AWS API 與 Kubernetes API。但「成功部署」和「production-ready」仍是兩件事。正式環境還需要容器與相依套件掃描、完整 IAM 設計、負載測試、告警、SLO、備份、升級、rollback 與失敗復原驗證。

後半段改用 AWS DevOps Agent 調查 EKS 故障，包括 CPU 壓力、回應變慢、JVM memory、OOM 與 Pod restart。Agent 可以把 EKS resources、Pod logs、events、node health 與 CloudWatch telemetry 放進同一條調查路徑，從自然語言問題一路追到可能的 root cause 與 mitigation plan。

這裡有一條很重要的邊界：AWS DevOps Agent 對 EKS 的整合是唯讀的。它可以查 resources、讀 logs、看 events、整理原因與建議，但不能直接建立、修改或刪除 cluster resources。這不是限制，反而是很合理的導入起點。調查可以加速，實際變更仍然經過原本的 review、deployment、rollback 與 post-validation 流程。

## AI Agent 會怎麼改變 DevOps 工作

### 1. 從寫自動化腳本，走向設計控制系統

傳統自動化通常由人先寫好固定步驟，再讓 pipeline 或 runbook 重複執行。Agent 則會根據目標與現況動態選擇工具。

DevOps 因此要往上一層設計：

- 任務意圖是什麼？
- 可以使用哪些資料與工具？
- 哪些動作需要核准？
- 成功條件和停止條件是什麼？
- 失敗時怎麼回復？
- 最後要留下哪些證據？

Shell、Terraform、Kubernetes 與 CI/CD 不會因此不重要。Agent 反而更依賴穩定、清楚且可預期的工具介面。原本含糊、缺乏錯誤處理、只有少數人知道怎麼用的 script，交給 Agent 後只會更難控制。

### 2. 開發速度提高，交付瓶頸會往後移

Coding Agent 可以加快程式碼、測試、容器與 manifest 的產生，但整體交付速度仍受 code review、security review、release window、環境容量與 incident response 影響。

如果只追蹤 coding throughput，很容易得到錯誤結論。更值得一起觀察的是：

- Lead time
- Review time
- Change failure rate
- Rollback rate
- Incident rate
- 修復後驗證時間

當前段突然加速，後段控制若沒有跟上，風險只會更快堆積。

### 3. Incident investigation 會比自動修復更早成熟

On-call 最耗時間的部分，常常不是執行修復指令，而是先弄清楚服務拓樸、找到正確的 dashboard、比對 deployment、查 logs、看 events，再排除彼此矛盾的線索。

Agent 很適合把這些資訊串起來，讓調查從「哪個服務變慢」開始，而不是要求人先知道正確的 CloudWatch query 或 Pod 名稱。

但 investigation、recommendation 與 remediation 應該是三個權限層級。我的理想導入順序會是：

1. 先開放唯讀資料，要求每個 finding 都附來源。
2. 讓 Agent 提出修復方案與風險，但不直接執行。
3. 低風險動作改成核准後執行。
4. 只有在可回復、可觀測且累積足夠成功紀錄後，才考慮自動執行。

### 4. Context 與 telemetry 會成為平台產品

Agent 的輸出品質取決於它拿到的脈絡。Service catalog、owner、dependency、SLO、runbook、deployment history、feature flag、incident、postmortem 與成本資料，以後不只是文件，而是 Agent 執行工作的輸入。

這些資料也需要品質管理。過期 runbook、錯誤 owner、缺漏 telemetry，都可能讓 Agent 很快得出錯誤答案。平台團隊除了建立 chat 或工具入口，也要處理資料新鮮度、引用來源、權限與可觀測性。

### 5. MCP 與工具供應鏈會成為日常風險

MCP 讓不同 Agent 用一致方式連接檔案、AWS、Kubernetes 與各種外部服務，但 MCP 本身不是安全邊界。MCP Server 仍可能執行本機程式、讀寫檔案、取得 credentials、連線外部服務或修改雲端資源。

正式環境至少要確認：

- 來源、版本與更新方式
- 實際暴露的 tool list
- IAM 與 credentials handling
- Filesystem 與 network access
- 操作 logs 與撤銷方式
- 寫入範圍與人工核准點

`trust-all` 類設定只適合可丟棄的沙盒，不適合拿來換取正式環境的方便。

### 6. Agent 越快，證據鏈越不能省

Agent 可以在短時間內跨越多個系統，因此除了 ticket、diff、review、test 與 deployment log，還要能回答：

- 它讀了哪些 context？
- 呼叫了哪些 tools？
- 採用了哪些假設？
- 產生或修改了哪些 artifacts？
- 人在什麼時間點核准了什麼？
- 部署後的系統狀態是否符合預期？

沒有這條證據鏈，就無法區分「Agent 說完成了」與「系統真的完成了」。

### 7. 模型成本與可用性也會進入 SRE 範圍

Agent 在規劃、執行與自我檢查時，可能在單一任務中多次呼叫模型。規模放大後，token 使用量、model latency、quota、throttling、tool failure、retry 與 session duration 都會影響成本和可靠度。

這類 workload 最後也需要 SLI、SLO、告警、成本歸屬與人工 fallback。否則 Agent 會從提升效率的工具，變成新的單點故障。

## 這些工具各自適合放在哪裡

| 工具或平台 | 適合處理的工作 | 需要自己守住的邊界 |
| --- | --- | --- |
| Amazon Quick | 串接 email、行事曆與企業資料，建立摘要、排程、自訂 Agent、瀏覽器操作與深度分析流程 | 資料授權、排序規則、排程失敗處理與高風險輸出覆核 |
| Kiro CLI | 依專案規則與工具介面完成程式碼、測試、容器與部署 artifacts | 規格品質、tool trust、IAM、供應鏈、測試深度與 production readiness |
| Amazon EKS Auto Mode | 管理更多 node、compute autoscaling、load balancing、networking 與 storage 基礎元件 | Application availability、security、monitoring、VPC 與 EKS 設定仍是自己的責任 |
| CloudWatch Container Insights | 蒐集與呈現 container、Pod、Node 與 cluster telemetry | Retention、告警、dashboard、SLO、成本與事件脈絡 |
| AWS DevOps Agent | 關聯 topology、metrics、logs、events、code 與 deployment，協助 incident investigation | EKS 整合為唯讀；實際變更、rollback 與驗證仍走既有流程 |
| AWS Transform | 協助 legacy analysis、文件整理、程式轉換與系統現代化 | 功能等價性、資料遷移、整合測試、效能、資安與切換證據 |
| Amazon Bedrock AgentCore | 提供 Agent runtime、memory、identity、policy、observability 與 evaluation 能力 | Agent logic、工具權限、資料品質、評估集與失敗處理 |
| Codex、Claude 等 Coding Agent | 分析 codebase、修改程式碼、執行測試並整理結果 | 規格、驗收條件、repository 權限、review、secret handling 與部署授權 |
| MCP | 讓 Agent 與不同工具用共同協定互通 | 來源、工具能力、credentials、network 與 filesystem access 都要另外治理 |

## 如果要在團隊裡開始，我會這樣做

1. **選一條窄而高價值的流程**：例如已知 incident 的唯讀 replay、pull request 風險摘要、變更前檢查或每日營運摘要。
2. **建立人工 baseline**：先記錄處理時間、正確率、誤判、人工步驟、成本與既有風險。
3. **把隱性知識外顯化**：整理 service owner、SLO、runbook、severity、escalation 與 rollback 規則，並設定版本和 owner。
4. **從唯讀工具開始**：要求 finding 附來源，測量可追溯性與人工覆核時間。
5. **把寫入拆成小能力**：限制 AWS account、Region、cluster、namespace、repository、branch、filesystem path 與 tool allowlist。
6. **用歷史事件做盲測**：挑選已有 postmortem 的 incidents，隱藏根因，評估 finding precision、調查時間、成本與錯誤建議。
7. **保留完整變更證據**：讓 diff、test、scan、deployment output、監控變化、rollback 與 post-validation 都能回查。
8. **最後才提高自主性**：只在低風險、可回復、可觀測且長期表現穩定的工作上擴大自動核准範圍。

## 結語

AWS Summit Taipei 2026 讓我更確定，DevOps 接下來面對的不是「AI 會不會取代工程師」，而是軟體交付與維運將從固定步驟的自動化，走向能根據脈絡規劃並使用工具的執行模式。

Agent 讓程式碼、部署與調查變快，也會讓錯誤權限、過期文件、缺漏監控與不完整驗證更快進入正式環境。真正可持續的做法，是把 Agent 放進規格、最小權限、change management、observability、testing 與 rollback 的系統裡，而不是用一個聊天介面繞過它們。

所以我不認為 DevOps 的角色會縮小。它會更靠近平台與控制系統的設計者：提供一條讓人與 Agent 都能安全完成工作、留下證據，並在失敗時回復的 paved path。
