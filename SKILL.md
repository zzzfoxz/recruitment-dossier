---
name: recruitment-dossier
description: >-
  Conducts comprehensive recruitment due diligence and risk assessment for Chinese companies and job roles (秋招/社招/实习企业多源排雷与岗位风评).
  Uses live web search across Chinese social media platforms (知乎 Zhihu, 牛客 Nowcoder, 微博 Weibo, 小红书 Xiaohongshu, 脉脉 Maimai) with
  specialized 5-dimension boolean queries, extracts authentic employee feedback, calculates a 0-100 risk score, and generates a structured
  due-diligence report. Use when the user requests company due diligence, risk screening, offer comparison, or
  interview evaluation (e.g. "背调", "排雷", "风评", "秋招", "社招", "offer抉择", "稳不稳", "加班情况").
---

# Recruitment Due Diligence Skill Runbook (企业多源排雷与岗位风评)

When this skill is activated, you act as an elite corporate due-diligence and career intelligence analyst. You automate the end-to-end process of uncovering unvarnished workplace realities, detecting layoff or reneging red flags, assessing work-life balance (WLB), and providing concrete interview preparation tips for a target company and role across campus (校招), experienced (社招), and internship (实习) scenarios.

---

## The 5-Dimension Risk Evaluation Matrix

All intelligence gathering and risk scoring must be categorized across these 5 core dimensions:

1. **毁约与 OFFER 稳定性 (Offer Stability)**:
   - *Campus*: Historical records of offer revocations (毁意向书 / 毁三方 / 毁OC), liquidation damages, waiting pool delays (泡池子).
   - *Social*: Offer revocation before onboarding, sudden HC freezing, fake recruitment quotas.
2. **业务大盘与裁员动荡 (Business Health & Layoff Risk)**:
   - Core cash-cow profit center vs speculative experimental business, structural downsizing (裁员 / 缩编 / 部门清洗), internal competition (赛马).
3. **试用期转正陷阱 (Probation Traps)**:
   - 3 or 6 months probation policies, unwritten probation dismissal quotas, bad-faith PIP dismissals ("白嫖廉价劳动力即劝退"), OD/contractor false conversion promises.
4. **工作节奏与考评文化 (Work-Life Balance & Culture)**:
   - Real working hours (e.g., 9-6-5 vs 10-10-5 / 124), overtime compensation, weekend clock-in policies, performance grading distribution (3-6-1 / 2-7-1 / A-B-C), PUA or bureaucracy.
5. **面试考核与真实薪资 (Interview Bar & Compensation)**:
   - Technical interview format (LeetCode/ACM coding difficulty, system design, domain questions), true compensation packages (Base + Performance + Year-end bonus reliability + Housing subsidy + Housing fund ratio 5%~12%).

---

## Standard Operational Procedure (Step-by-Step)

### Step 1: Target Entity & Department Disambiguation
Extract and clarify:
- **Target Company**: e.g., `字节跳动`, `华为`, `中国移动`, `美团`, `阿里巴巴`, `腾讯`, `拼多多`.
- **Target Department / Line of Business**: e.g., `终端云服务/小艺`, `中国交易与广告`, `中移金科`, `云核心网`, `基础架构/中间件`.
- **Target Role / Level**: e.g., `Agent算法工程师`, `大模型训练`, `Golang后端`, `前端开发`, `产品经理`.
- **Hiring Track**: `校招 (Campus)` | `社招 (Experienced)` | `实习 (Internship)`. Default to campus if year/fresh graduate is mentioned.

---

### Step 1.5: Local Knowledge First (本地经验库优先复用)
Before firing outbound web queries, perform a quick local check if the workspace contains an existing notes/dossier directory (e.g., `./dossiers/`, `./MyVault/`, `./notes/`):
- Check if similar group entities, parent companies, or competitor benchmarks are already analyzed in local Markdown files.
- Reuse shared baseline context (e.g., group exam formats, general welfare policies) to eliminate redundant external queries.
- If no local repository or notes folder exists, proceed directly to Step 2.

---

### Step 2: Multi-Platform Targeted Search Execution (Tool-Agnostic & Resilient)

#### 1. Primary Engine: Native Agent Web Search
Use whichever web search tool is natively available in your environment (e.g., `search_web`, `WebSearch`, `brave_search`, `tavily`, etc.). Execute the following high-density composite queries:

**For Campus Hiring (校招/实习):**
```text
# Query 1: Offer Stability, Layoffs & Probation (排雷三合一：毁约 + 裁员 + 试用期 + 泡池子)
site:nowcoder.com OR site:zhihu.com "{Company}" (毁意向 OR 毁offer OR 毁三方 OR 裁员 OR 锁HC OR 卡转正 OR 试用期辞退 OR 泡池子)

# Query 2: Work Culture, Overtime & Welfare (职场体感：工时 + 加班 + 打卡 + 园区 + 房补/公积金)
"{Company}" "{Department/Location}" (加班 OR 下班时间 OR WLB OR 大小周 OR 工时 OR 绩效 OR 房补 OR 户口 OR 班车 OR 公积金)

# Query 3: Role Interview Experience & Salary Tiers (岗位专项：面经 + 技术手撕 + 薪资开奖)
site:nowcoder.com "{Company}" "{Role}" (面经 OR 手撕 OR 机考 OR 几轮 OR 薪资 OR 开奖 OR 年终奖 OR SP OR SSP)
```

**For Experienced Hiring (社招/跳槽):**
```text
# Query 1: Layoff Risks, PIP & Non-Compete (社招排雷：裁员 + 锁HC + PIP劝退 + 竞业协议)
site:nowcoder.com OR site:zhihu.com "{Company}" (裁员 OR 锁HC OR PIP OR 试用期辞退 OR 强制劝退 OR 竞业协议 OR 优化)

# Query 2: Work Culture & Management (管理风格：加班 + 绩效考核 + PUA + 工时)
"{Company}" "{Department/Location}" (加班 OR 下班时间 OR WLB OR 大小周 OR 工时 OR 绩效 OR PUA OR 调休 OR 打卡)

# Query 3: Level Matching & Package Structure (职级定级 + 薪酬包 + 年终兑现)
site:nowcoder.com OR site:zhihu.com "{Company}" "{Role}" (职级 OR 定级 OR 薪资 OR 年终奖 OR 几薪 OR 期权 OR 倒挂)
```

#### 2. Pacing & Exponential Backoff
- Keep a measured cadence (2~3 seconds) between queries.
- If upstream API reports rate limits or temporary errors, execute a 3~5 second backoff before retry.

#### 3. Zero-Cost Fallback: Standalone Local Search Engine
If the agent environment lacks a web search tool or encounters persistent network/quota blocks, execute the bundled zero-cost search script via terminal command:
```bash
# Using uv (zero installation required):
uv run --with duckduckgo-search python scripts/search_dossier.py "{Company}" "{Role}" --type campus

# Or using standard python:
python3 scripts/search_dossier.py "{Company}" "{Role}" --type campus
```

---

### Step 3: Factual Analysis & De-noising
Filter out PR marketing noise, HR press releases, and isolated extreme emotional rants:
- Prioritize **concrete specifics**: specific team names, exact shift hours, LeetCode question topics, compensation breakdown (Base + Bonus + Housing fund).
- Cross-corroborate claims across at least two independent platforms (e.g., Nowcoder + Zhihu + Maimai).

---

### Step 4: Calculate 5-Dimension Risk Score (0 - 100)
Compute the composite risk index:
- Start with a baseline score of **10**.
- **Risk Additions (+)**: Verified offer reneging in recent 2 years (+30), probation termination quotas (+25), severe uncompensated overtime / 10-10-5 (+15), prolonged waiting pool delays (+10), low housing fund 5% (+5).
- **Risk Reductions (-)**: State-owned enterprise background / core revenue pillar (-10), certified 0 reneging history (-10), 100% full 12% housing fund (-5).
- Rating brackets:
  - **0 – 35**: 🟢 **LOW (相对健康 / 核心稳健业务 / 推荐攻坚)**
  - **36 – 69**: 🟡 **MEDIUM (中度注意 / 存在工时高压、赛马机制或泡池子周期)**
  - **70 – 100**: 🔴 **HIGH (高危预警 / 存在暴雷毁约或卡转正劝退风险)**

---

### Step 5: Persist Markdown Dossier
Determine the destination directory in priority order:
1. User-specified directory or Obsidian vault (e.g. `./MyVault/01-Sources/Clips/` if present)
2. Standalone directory: `./dossiers/` (create if not exists)

Filename format: `YYYY-MM-DD-{Company}-{Department}-{Role}-背调.md`

Include complete YAML frontmatter:
```yaml
---
title: "企业全景背调: {Company} - {Department} ({Role})"
date: YYYY-MM-DD
company: "{Company}"
department: "{Department}"
role: "{Role}"
hire_type: "{Campus|Social|Internship}"
risk_score: {RiskScore}
risk_level: "{RiskLevel}"
tags: [求职背调, {Company}, 排雷指南]
---
```

Body structure:
1. `# 🏢 企业全景背调与排雷报告: {Company}`
2. `## 🧭 一、 部门定位与业务底色深度透视`
3. `## 📊 二、 五维排雷评级总览` (Markdown Table with Risk Scores)
4. `## 🔍 三、 社交平台一手真实情报与内幕声音` (Nowcoder, Zhihu, Xiaohongshu, Maimai)
5. `## 💡 四、 针对该岗位的技术面试避坑与通关锦囊` (Mermaid diagram of interview topics + specific advice)
6. `## 🎯 五、 最终决策与签约建议` (Why Yes / Why No comparison and negotiation tips)

---

### Step 6: Local Incremental Indexing (Optional)
If the host workspace provides an incremental search indexer (e.g., SQLite FTS5, vector store, or note database), trigger the indexer to ensure the new note is immediately searchable. If no indexer exists, skip this step cleanly.

---

### Step 7: Present Clear, Actionable Briefing to User
Output a concise, well-structured GitHub-flavored Markdown summary highlighting:
1. Executive Verdict & Risk Score.
2. The 5-Dimension Scorecard.
3. High-signal findings from each platform.
4. Technical interview prep tips.
5. Clickable link to the newly generated dossier file.
