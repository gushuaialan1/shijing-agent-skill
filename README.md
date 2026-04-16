# 史镜 Agent Skill — Historical Empathy Agent

> **用原典托底，用细节入场，用词眼转动，用古今对照扩容，用情绪弧线收束，再用事实边界保真。**
> Anchor in classics, enter through details, turn with key words, bridge ancient and modern, arc the emotion, and stay true to facts.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Skill Version](https://img.shields.io/badge/version-1.0.0-green.svg)](#)

---

## 特色 | Features

- **史料锚定 | Evidence-based** — 以原典、时间、地点、制度处境为基座，拒绝空泛情绪
- **镜头化取样 | Cinematic Sampling** — 不写一生概括，只捞一个“一秒钟能拍出来”的决定性瞬间
- **词眼拆解 | Word-level Dissection** — 拉动人格显形的动词、虚词、转折词
- **古今对照 | Cross-era Bridge** — 系统级关系类比，而非表面比附
- **情绪编排 | Emotional Arc** — 压迫、停顿、翻转、回望的四段式节奏

---

## 快速上手 | Quick Start

```bash
# 1. Clone 技能到本地 Hermes skills 目录
cd ~/.hermes/skills
git clone https://github.com/gushuaialan1/shijing-agent-skill.git

# 2. 在 Hermes 中加载
/skills
```

然后发送任务：

```text
用史镜 Agent 写一篇关于苏轼《定风波》的深描文案，面向职场困境中的年轻人，成稿约 1200 字。
```

---

## 演示 | Demo

**输入（Input）**
> 人物：苏轼 | 文本：《定风波》 | 受众：25-35 岁职场人 | 困境：失业/转行压力

**输出（Output）**
> 硬事实卡 → 微场景（沙湖道中遇雨） → 词眼卡（莫听、何妨、轻胜马、谁怕、任平生） → 古今对照卡 → 情绪曲线 → 1200 字成稿 → 五问终审

---

## 架构说明 | Architecture

| 层面 | 技术 | 说明 |
|:---|:---|:---|
| 技能定义 | Markdown + YAML Frontmatter | Hermes Skill 标准格式 |
| 提示词模板 | Markdown 模板 | 结构化 LLM Prompt，包含 7 步工作流与五问质检 |
| 辅助工具 | Python 3.10+ | CLI 脚本，支持 JSON/YAML 配置与结构化报告输出 |

---

## 安装 | Installation

### Hermes 用户

将本仓库克隆到 `~/.hermes/skills/shijing-agent-skill`，然后在会话中使用 `/skills` 命令列出已加载技能。

### 独立使用 CLI

```bash
cd shijing-agent-skill
pip install pyyaml  # 可选，用于加载 YAML 配置
python scripts/shijing_agent.py --help
```

---

## 用法示例 | Usage

### 方式一：Hermes 技能调用

直接发送自然语言任务，Hermes 会自动匹配并加载 `shijing-agent` skill。

### 方式二：CLI 脚本

**使用命令行参数**

```bash
python scripts/shijing_agent.py \
  --character "苏轼" \
  --text "定风波" \
  --audience "职场人" \
  --problem "失业焦虑" \
  --length 1200 \
  --format markdown \
  --output report.md
```

**使用 YAML 配置**

```bash
python scripts/shijing_agent.py --config task.yaml --format json --output report.json
```

---

## 配置 | Configuration

创建 `task.yaml`：

```yaml
character: "苏轼"
text: "定风波"
audience: "25-35 岁职场人"
problem: "失业与转行压力"
length: 1200
```

---

## 开发指南 | Development

1. 阅读 `references/` 目录下的研究文档，理解史镜 Agent 的理论基础
2. 修改 `SKILL.md` 或 `templates/prompt.md`以调整技能行为
3. 本地验证：将技能复制到 `~/.hermes/skills/shijing-agent-skill`，重新加载 Hermes
4. 运行 CLI 脚本，检查输出格式与结构是否正确

---

## 路线图 | Roadmap

- [x] 研究阶段：完成原文、深度报告、解析框架
- [x] 技能化：产出 `SKILL.md` + 提示词模板
- [x] 工具化：完成 CLI 辅助脚本
- [ ] 验证：内部测试与迭代
- [ ] 发布：v1.1.0 增强版本

---

## 文档与示例 | Docs & Examples

| 文档 | 说明 |
|:---|:---|
| [PROJECT_BRIEF.md](PROJECT_BRIEF.md) | 项目落地规划与验收标准 |
| [references/deep-research-report.md](references/deep-research-report.md) | 可复制框架研究报告 |
| [references/detailed-analysis-framework.md](references/detailed-analysis-framework.md) | 五层递进模型详解 |
| [references/source-text.txt](references/source-text.txt) | 《定风波》深描口播文案原文 |

---

## 授权与致谢 | License & Credits

MIT License 2026 gushuaialan1

本技能的理论基础来源于古典文本细读、叙事共情与古今类比研究。
