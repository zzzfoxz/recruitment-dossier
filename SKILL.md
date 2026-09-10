---
name: recruitment-dossier
description: >-
  Conducts comprehensive recruitment due diligence and risk assessment for Chinese companies and job roles (秋招/社招企业排雷与岗位风评).
  Uses live web search across Chinese social media platforms (知乎 Zhihu, 牛客 Nowcoder, 微博 Weibo, 小红书 Xiaohongshu, 脉脉 Maimai) with
  specialized 5-dimension boolean queries, extracts authentic employee feedback, calculates a 0-100 risk score, and generates a structured
  due-diligence report archived into MyVault. Use when the user requests company due diligence, risk screening, offer comparison, or
  interview evaluation (e.g. "背调", "排雷", "风评", "秋招", "offer抉择", "稳不稳", "加班情况").
---

# Recruitment Due Diligence Skill Runbook (秋招企业多源排雷与岗位风评)

When this skill is activated, you act as an elite corporate due-diligence and career intelligence analyst. You automate the end-to-end process of uncovering unvarnished workplace realities, detecting layoff or reneging red flags, assessing work-life balance (WLB), and providing concrete interview preparation tips for a target company and role.

---

## The 5-Dimension Risk Evaluation Matrix

All intelligence gathering and risk scoring must be categorized across these 5 core dimensions:

1. **毁约与 OFFER 稳定性 (Offer Stability)**:
   - Historical records of offer revocations (毁意向书 / 毁三方 / 毁OC), compensation for liquidated damages, last-minute cancellation before onboarding.
2. **业务大盘与裁员动荡 (Business Health & Layoff Risk)**:
   - Core cash-cow profit center vs speculative experimental business, structural downsizing (裁员 / 缩编 / 锁HC / 部门清洗), internal competition (赛马).
3. **试用期转正陷阱 (Probation Traps)**:
   - 3 or 6 months probation policies, unwritten probation dismissal quotas, bad-faith PIP dismissals ("白嫖廉价劳动力即劝退").
4. **工作节奏与考评文化 (Work-Life Balance & Culture)**:
   - Real working hours (e.g., 9-5.5-5 vs 10-10-5), overtime allowances, weekend clock-in policies, 3-6-1 / 2-7-1 performance grading, PUA or bureaucracy.
5. **面试考核与真实薪资 (Interview Bar & Compensation)**:
   - Technical interview format (LeetCode coding difficulty, system design, domain questions), true compensation packages (Base + Performance + Year-end bonus reliability + Housing subsidy + Full 12% housing fund).

---

## Standard Operational Procedure (Step-by-Step)

### Step 1: Target Entity & Department Disambiguation
Extract and clarify:
- **Target Company**: e.g., `字节跳动`, `中国移动`, `华为`, `美团`, `阿里巴巴`, `拼多多`, `得物`.
- **Target Department / Line of Business**: e.g., `中国交易与广告`, `中移金科`, `云核心网`, `到家事业群`, `基础架构/中间件`.
- **Target Role / Level**: e.g., `Agent算法工程师`, `中间件AI开发`, `服务端开发`, `前端`, `产品经理`.

---

### Step 1.5: Local Knowledge First (本地经验库优先复用)
Before firing outbound web queries, perform a quick local scan using `ext-vault-search.ts` on `MyVault/01-Sources/Clips/`:
- Check if similar group entities, parent companies, or competitor benchmarks are already analyzed (e.g., existing China Mobile group exam rules, ByteDance performance grading, Alibaba 88VIP architecture).
- Reuse shared baseline context (group exam formats, general welfare frameworks) to eliminate redundant external queries.

---

### Step 2: Multi-Platform Targeted Search Execution (Anti-503 & Rate Limit Resilient)
To prevent backend model capacity exhaustion (`503 Service Unavailable / MODEL_CAPACITY_EXHAUSTED`) and avoid platform anti-bot triggers:

#### 1. High-Density Synthesized Queries (高维合成布尔查询，将 5 次调用压缩为 2~3 次)
Consolidate atomic queries into comprehensive composite expressions:

```text
# Composite Query 1: Offer Stability, Layoffs & Probation Traps (排雷三合一：毁约 + 裁员 + 试用期)
site:nowcoder.com OR site:zhihu.com "{Company}" (毁意向 OR 毁offer OR 毁三方 OR 裁员 OR 锁HC OR 卡转正 OR 试用期辞退)

# Composite Query 2: Work Culture, Overtime, Location & Welfare (职场体感：工时 + 加班 + 打卡 + 园区 + 户口/房补)
"{Company}" "{Department/Location}" (加班 OR 下班时间 OR WLB OR 大小周 OR 工时 OR 绩效 OR 房补 OR 户口 OR 班车)

# Composite Query 3: Role Interview Experience & Compensation Tiers (岗位专项：面经 + 技术手撕 + 薪资开奖)
site:nowcoder.com "{Company}" "{Role}" (面经 OR 手撕 OR 几轮 OR 薪资 OR 开奖 OR 年终奖 OR SP OR SSP)
```

#### 2. Pacing & Exponential Backoff Governance (频控平滑与指数退避)
- **Request Pacing**: Avoid rapid burst calls within < 2 seconds. Keep a measured cadence between queries.
- **503 / 429 Exception Handling**:
  - If a tool output reports `503 Service Unavailable` or `MODEL_CAPACITY_EXHAUSTED`, **NEVER retry immediately within 1 second**.
  - Execute a 3~5 second backoff interval before the next attempt.
  - Prioritize executing local context parsing or file preparation during the wait.

#### 3. Ultimate Fallback: Local DDGS Engine (终极备选方案：本地 ddgs 离线引擎)
If `search_web` model capacity remains exhausted (`503 Service Unavailable`) after backoff attempts (≥ 2 failures), immediately activate the **local DDGS zero-cost fallback engine** via `run_command`:
- **Advantage**: 0 API Key required, 100% free, immune to cloud model quota limits, employs Rust TLS client impersonation (`primp`) to bypass anti-bot blocks.
- **Execution Command**:
  ```bash
  /Users/admin/.local/bin/uv run --with ddgs python -c "
  import json, sys
  from ddgs import DDGS
  query = '''{Query}'''
  try:
      results = DDGS().text(query, max_results=5)
      print(json.dumps([{'title': r['title'], 'href': r['href'], 'body': r['body']} for r in results], ensure_ascii=False, indent=2))
  except Exception as e:
      print(f'DDGS error: {e}', file=sys.stderr)
  "
  ```
- Parse the resulting JSON directly (`title`, `href`, `body`) to extract interview questions, salary packages, and probation feedback.
- If a target URL requires deep reading, follow up with `read_url_content`.

---

### Step 3: Factual Analysis & De-noising
Filter out PR marketing noise, official press releases, and extreme emotional rants:
- Look for **concrete specifics**: specific team code names, exact shift hours, LeetCode question topics, compensation numbers (k/month, months of bonus).
- Corroborate claims across at least two independent platforms (e.g., Nowcoder discussion + Zhihu retrospective).

---

### Step 4: Calculate 5-Dimension Risk Score (0 - 100)
Compute the composite risk index:
- Start with a baseline score of 10.
- For each verified high-risk signal (offer reneging in recent 2 years, probation termination scandals, severe uncompensated overtime), add 20–40 points.
- For verified mitigating factors (state-owned enterprise background, core revenue generator, 100% full housing fund, zero reneging history), reduce risk points.
- Rating brackets:
  - **0 – 35**: 🟢 **LOW (相对健康 / 稳健推荐)**
  - **36 – 69**: 🟡 **MEDIUM (中度注意 / 存在节奏或赛马压力)**
  - **70 – 100**: 🔴 **HIGH (高危预警 / 存在暴雷毁约或卡转正风险)**

---

### Step 5: Persist Markdown Dossier into Knowledge Vault
Write the completed dossier to `./MyVault/01-Sources/Clips/`:
Filename format: `MyVault/01-Sources/Clips/YYYY-MM-DD-{Company}-{Department}-{Role}-秋招背调.md`

Include complete YAML frontmatter:
```yaml
---
title: "秋招企业全景背调: {Company} - {Department} ({Role})"
date: YYYY-MM-DD
company: "{Company}"
department: "{Department}"
role: "{Role}"
risk_score: {RiskScore}
risk_level: "{RiskLevel}"
tags: [秋招背调, {Company}, 排雷指南]
---
```

Body structure:
1. `# 🏢 企业全景背调与排雷报告: {Company}`
2. `## 🧭 一、 部门定位与业务底色深度透视`
3. `## 📊 二、 五维排雷评级总览` (Markdown Table with Risk Scores)
4. `## 🔍 三、 社交平台一手真实情报与内幕声音` (Nowcoder, Zhihu, Xiaohongshu, Maimai, Weibo)
5. `## 💡 四、 针对该岗位的技术面试避坑与通关锦囊` (Mermaid diagram of high-frequency interview topics)
6. `## 🎯 五、 最终决策与签约建议` (A/B/C tier verdict and negotiation strategy)

---

### Step 6: Trigger Local Incremental Indexing
After writing the file, run a quick vault search check using Node.js to ensure the new note is immediately indexed in the SQLite FTS5 + vector BLOB + RRF database:
```bash
node -e 'import("./ext-vault-search.ts").then(m => m.searchVault("{Company} {Role}"));'
```

---

### Step 7: Present Clear, Actionable Briefing to User
Output a concise, well-structured GitHub-flavored Markdown summary highlighting:
1. Executive Verdict & Risk Score.
2. The 5-Dimension Scorecard.
3. High-signal findings from each platform.
4. Technical interview prep tips.
5. Clickable link to the newly generated file in `MyVault`.
