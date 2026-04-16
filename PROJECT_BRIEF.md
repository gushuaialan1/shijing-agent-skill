# 史镜 Agent Skill — 项目落地规划

## 背景

我们已完成对《定风波》古今对照文案的深度研究，产出了三份核心资产：

1. `references/source-text.txt` — 原文口播文案（苏轼《定风波》深描样本）
2. `references/deep-research-report.md` — 《历史人物深描文案的可复制框架》研究报告，提出“史镜 Agent”与 7 步工作流
3. `references/detailed-analysis-framework.md` — 五层递进模型、修辞策略、情感节奏与可迁移框架的完整拆解

本项目目标：将上述研究成果**落地为一个可安装、可复用的 Hermes Skill**。

---

## 目标交付物

| 交付物 | 说明 | 优先级 |
|:---|:---|:---|
| `SKILL.md` | Hermes Skill 主文件。必须包含标准 YAML frontmatter + Trigger + Steps + Pitfalls + Verification | P0 |
| `templates/prompt.md` | 史镜 Agent 的完整提示词模板，可直接被 LLM 调用 | P0 |
| `scripts/shijing_agent.py` | 辅助脚本：提供 7 步工作流的结构化输入与输出格式化（CLI 工具） | P1 |
| `README.md` | 双语项目说明（符合 PM Standard） | P0 |

---

## Skill 核心设计

### 名称
`shijing-agent`（史镜 Agent）

### 一句话定位
围绕历史人物与经典文本，生成具备“史料锚定 + 镜头化取样 + 词眼拆解 + 古今对照 + 情绪编排”的深描型情绪文案。

### 工作流（7 步）
1. **定题** — 明确人物、文本、当代情绪、受众、字数
2. **取证** — 输出硬事实卡（原典、时间、地点、制度处境、争议点）
3. **选口** — 选一个最小、最硬、最能折射人物的瞬间
4. **拆句** — 关键句四栏解析：字面意思、现场动作、心理位移、现代映射
5. **搭桥** — 每个历史细节只配一个现代问题，避免硬扯
6. **成稿** — 按“当下困境 → 历史现场 → 逐句拆解 → 古今对照 → 情绪翻转 → 落到心法”结构输出文案
7. **终审** — 五问质检（瞬间可见？坐标成立？回得去原文？系统同构？可执行心法？）

### 风格约束
- 不神化人物，不乱改原句，不把现代价值观硬塞回古人
- 句式口语化，但证据链完整
- 结尾给出可执行的心法，而不是空泛鼓励

---

## 验收标准

- [ ] `SKILL.md` 可以被 Hermes 的 skill 系统正常加载（YAML frontmatter 合法）
- [ ] `SKILL.md` 正文完整覆盖 Trigger、Steps、Pitfalls、Verification 四部分
- [ ] `templates/prompt.md` 包含可直接投递给 LLM 的完整提示词（含 7 步工作流与五问质检）
- [ ] `scripts/shijing_agent.py` 能在命令行运行，接受 JSON/YAML 配置并输出结构化结果
- [ ] `README.md` 双语、符合 PM Standard（Hero line / Badges / Features / Quick Start / Demo / Architecture / Installation / Usage / Config / Dev guide / Roadmap / License）
- [ ] 所有代码与文档无错别字、无格式错误

---

## 工作分配

### Phase 1 — 实现（Claude Code）
负责：
- 阅读 `references/` 下的三份研究文档
- 撰写 `SKILL.md` 与 `templates/prompt.md`
- 实现 `scripts/shijing_agent.py`（CLI 工具）
- 完善 `README.md`
- 提交到本仓库

### Phase 2 — Review（Codex）
负责：
- 对 `SKILL.md`、模板、脚本、README 进行 code review
- 检查是否符合 Hermes skill 规范
- 检查是否遗漏研究报告中的关键方法论
- 提交 review 意见或直接 PR 修复

---

## 参考规范

- Hermes Skill 格式：YAML frontmatter + markdown body（Trigger / Steps / Pitfalls / Verification）
- PM Standard README： bilingual（zh + en），13 个标准模块
