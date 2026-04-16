---
name: shijing-agent
description: "史镜 Agent — 历史人物深描型情绪文案生成技能"
version: 2.0.0
author: gushuaialan1
license: MIT
category: creative
metadata:
  hermes:
    tags: [content-creation, historical-narrative, empathy, short-video]
---

# 史镜 Agent (Shijing Agent)

> 本 Skill 采用**渐进式工作流**，零 LLM API 依赖。它提供分阶段的 Prompt 模板与数据验证工具，由宿主 Agent 分次调用 LLM 完成创作。

围绕历史人物与经典文本，生成具备"史料锚定 + 镜头化取样 + 词眼拆解 + 古今对照 + 情绪编排"的深描型情绪文案。

## Trigger: when to use this skill

当用户请求以下类型的内容时，激活本技能：

- 基于历史人物/经典文本的短视频口播文案、图文推文或播客脚本
- 需要将古代人物命运与当代情绪困境建立共鸣的"古今对照"文案
- 面向特定受众（职场人、学生、创业者等）的治愈型或认知重构型内容
- 用户提及"史镜"、"深描"、"历史人物文案"、"诗词解读"、"情绪文案"等关键词
- 要求内容兼具史料可信度与情感感染力的创作任务

不适用场景：纯学术考据、虚构架空创作、无历史文本支撑的空泛鸡汤。

## Progressive Workflow

为了减少单次 LLM 调用的 token 压力，提高输出质量，本 Skill 将创作流程拆分为 **5 个渐进 Stage**。宿主 Agent 可以分多次调用 LLM，每次只提交一个精简 prompt，逐步积累状态。

| Stage | 模块名 | 职责 | 依赖 |
|:---|:---|:---|:---|
| 1 | `setup` | 定题 + 取证 | 用户五要素 |
| 2 | `scene` | 选口（微场景） | stage_1 输出 |
| 3 | `dissect` | 拆句 + 搭桥 | stage_1 + stage_2 输出 |
| 4 | `compose` | 成稿 | stage_1/2/3 输出 |
| 5 | `review` | 终审（五问质检） | stage_4 输出 |

### 使用方式

1. 宿主 Agent 调用 `shijing_agent.py stage 01_setup --character ... --text ...`获取 prompt
2. 将 prompt 投给 LLM，获取输出，提取为 JSON
3. 保存 JSON 状态文件
4. 下一个 stage 时使用 `--input <上一步的 JSON>`继续
5. 可使用 `validate` 对每个 stage 的输出进行 JSON Schema 校验

## Stage Reference

| Stage | 关键输入 | 关键输出 | 约束 |
|:---|:---|:---|:---|
| `01_setup` | character, text, audience, problem, length | `hard_facts` (source_text, time, place, institutional_context, controversies) | 硬事实5项不能缺 |
| `02_scene` | 前序 hard_facts | `micro_scene` (selected_moment, actions, others_reaction, dramatic_tension, visual_elements) | 必须是可视觉化的最小瞬间 |
| `03_dissect` | 前序 hard_facts + micro_scene | `keyword_card` (3-5 条) + `ancient_modern_bridge` | 优先动词/虚词；古今对照必须标注映射类型 |
| `04_compose` | 前序所有状态 | `final_copy` + `emotional_arc` (4 阶段) | 结构为困境→现场→拆句→对照→翻转→心法 |
| `05_review` | stage_4 输出 | `final_review` (5 问答案) + `verdict` (PASS / NEEDS_REVISION) | 全部"是"才能 PASS |

## Data Contract

完整状态 JSON 结构如下：

```json
{
  "character": "string",
  "text": "string",
  "audience": "string",
  "problem": "string",
  "length": "string",
  "hard_facts": {
    "source_text": "string",
    "time": "string",
    "place": "string",
    "institutional_context": "string",
    "controversies": "string"
  },
  "micro_scene": {
    "selected_moment": "string",
    "actions": "string",
    "others_reaction": "string",
    "dramatic_tension": "string",
    "visual_elements": "string"
  },
  "keyword_card": [
    {
      "word": "string",
      "literal_meaning": "string",
      "on_scene_action": "string",
      "psychological_shift": "string",
      "modern_mapping": "string"
    }
  ],
  "ancient_modern_bridge": [
    {
      "historical_detail": "string",
      "modern_issue": "string",
      "mapping_type": "系统映射 | 字面联想"
    }
  ],
  "final_copy": "string",
  "emotional_arc": {
    "oppression": "string",
    "confrontation": "string",
    "pause": "string",
    "flip_or_retrospect": "string"
  },
  "final_review": {
    "q1_visible_moment": { "answer": true, "reason": "string" },
    "q2_coordinate_valid": { "answer": true, "reason": "string" },
    "q3_back_to_source": { "answer": true, "reason": "string" },
    "q4_structural_isomorphism": { "answer": true, "reason": "string" },
    "q5_actionable_insight": { "answer": true, "reason": "string" }
  },
  "verdict": "PASS"
}
```

## Pitfalls: common mistakes

### 1. 神化人物
把历史人物写成无所畏惧的完人，失去脆弱性和复杂性。结果：读者无法认同，智慧失去参考价值。

**修正**：保留人物的"微冷"时刻——他也会怕、也会累、也会迷茫。

### 2. 鸡汤化
把经典文本简化为空洞口号（"只要你达观，一切都会好"），丢失原文的张力和历史语境。

**修正**：每一句高光都必须有史料和具体场景托底。

### 3. 古今强拉
为了蹭热点，把现代概念生搬进古代场景（"苏轼在职场被 PUA"）。对照失去可信度。

**修正**：古今对照必须基于关系结构的同构，并明确标注映射类型。

### 4. 无史料
没有原典、没有时间线、没有地理和制度坐标，只剩情绪表演。

**修正**：先输出硬事实卡，再动笔写文案。

### 5. 误引错字
为了口播爽感随意改字、错序、误引（如把"轻胜马"写成"青胜马"）。一处硬伤足以让全文 credibility 崩塌。

**修正**：成稿后逐句核对原文，确保引用准确。

## Verification: checklist for quality

- [ ] 五要素（人物、文本、情绪、受众、字数）在开头已明确
- [ ] 硬事实卡包含原典、时间、地点、制度处境、争议点
- [ ] 微场景是一个可视觉化的"最小瞬间"，包含具体动作和他人反应
- [ ] 词眼卡优先拆解动词、虚词、转折词，而非景物名词
- [ ] 古今对照卡中，每个历史细节只对应一个现代问题
- [ ] 古今对照基于"关系结构同构"，并明确说明
- [ ] 成稿包含"困境→现场→拆句→对照→翻转→心法"六段结构
- [ ] 情绪曲线至少包含四次变化（压迫、对抗、停顿、翻转/回望）
- [ ] 结尾给出可执行心法，不是空泛鼓励
- [ ] 五问质检全部回答"是"
- [ ] 无引文错误、无事实硬伤、无过度鸡汤化表达
