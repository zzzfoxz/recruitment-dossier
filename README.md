# 🕵️‍♂️ recruitment-dossier

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Agent: Skill](https://img.shields.io/badge/Agent-Skill-purple.svg)](SKILL.md)

秋招与社招企业多源排雷、岗位风评与技术面试尽调 Agent Skill。穿透公关营销与信息差，聚合多源社区真实爆料，量化五维风险，自动生成深度排雷报告与面试避坑指南。

---

## ⚡ 核心能力

- **五维风险量化 (0-100)**：覆盖「Offer稳定性、业务动荡、转正陷阱、工时节奏、面试与真实薪资」五大维度。
- **多源真实情报**：定向聚合牛客、脉脉同事圈、知乎与小红书的一手员工反馈，自动交叉验证与去噪。
- **面试与签约避坑**：输出高频技术考察矩阵（Mermaid 图谱）、机考/测评保命法则与 Offer 谈判策略。
- **双引擎搜索保障**：支持宿主 Agent 云端联网搜索，内置本地零秘钥 DuckDuckGo 引擎兜底。

---

## 🚀 快速安装

本 Skill 遵循通用 Agent 规范，支持一键引入：

### Google Antigravity (AGY)
```bash
mkdir -p ~/.gemini/config/skills/recruitment-dossier
cp SKILL.md ~/.gemini/config/skills/recruitment-dossier/
```

### Claude Code
```bash
mkdir -p ~/.claude/skills/recruitment-dossier
cp SKILL.md ~/.claude/skills/recruitment-dossier/
```

### Cursor / Windsurf / Trae
* **Cursor**: 复制 `SKILL.md` 内容至 `.cursor/rules/recruitment-dossier.mdc`
* **Windsurf**: 添加至 `.windsurfrules`

---

## 💡 使用方式

在对话中直接发送企业与目标岗位需求即可触发：

```text
/recruitment-dossier 华为 终端小艺 模型训练与Agent开发
/recruitment-dossier 字节跳动 商业化技术 Agent算法工程师
```

---

## 📘 产出样例

调研完成后自动沉淀结构化 Markdown 排雷报告：
* 样例参考：[华为终端小艺大模型与Agent开发背调报告](examples/example-dossier-huawei.md)

---

## 📄 开源许可

基于 [MIT License](LICENSE) 开源。
