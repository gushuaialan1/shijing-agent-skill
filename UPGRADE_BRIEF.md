# 史镜 Agent Skill v2.0 升级规划

## 目标

将当前 monolithic 的 7-step prompt 升级为 **渐进式、模块化的 5-Stage 工作流 Skill**。满足：

1. **模块独立**：每个 stage 有独立的 prompt 模板、输入 schema、输出 schema
2. **渐进式 token 提交**：宿主 Agent（Hermes/Claude/IDE）可分多次调用 LLM，每次只发一个精简 prompt
3. **零 LLM API 依赖**：Skill 本身不调任何模型，只负责生成 prompt、验证数据格式、编排流程
4. **每个模块真实发挥作用**：有可执行脚本、stage 间数据流转、JSON Schema 校验

---

## 5-Stage 架构

| Stage | 模块名 | 职责 | 依赖 |
|:---|:---|:---|:---|
| 1 | `setup` | 定题 + 取证 | 用户五要素 |
| 2 | `scene` | 选口（微场景） | stage_1 输出 |
| 3 | `dissect` | 拆句 + 搭桥 | stage_1 + stage_2 输出 |
| 4 | `compose` | 成稿 | stage_1/2/3 输出 |
| 5 | `review` | 终审（五问质检） | stage_4 输出 |

---

## 文件结构（目标）

```
shijing-agent-skill/
├── SKILL.md
├── README.md
├── PROJECT_BRIEF.md
├── UPGRADE_BRIEF.md
├── references/
├── templates/
│   ├── prompts/
│   │   ├── stage_01_setup.md
│   │   ├── stage_02_scene.md
│   │   ├── stage_03_dissect.md
│   │   ├── stage_04_compose.md
│   │   └── stage_05_review.md
│   └── schemas/
│       ├── stage_01_setup.json
│       ├── stage_02_scene.json
│       ├── stage_03_dissect.json
│       ├── stage_04_compose.json
│       └── stage_05_review.json
└── scripts/
    ├── shijing_agent.py              # Orchestrator CLI
    └── lib/
        ├── __init__.py
        ├── prompt_builder.py         # 按 stage 构建 prompt
        ├── validator.py              # JSON Schema 验证
        └── state.py                  # 读取/保存/合并 stage 状态
```

---

## 详细交付标准

### 1. Prompt 模板 (`templates/prompts/stage_*.md`)

每个模板必须：
- 只包含该 stage 的**单一职责**说明
- 引用前序 stage 的**关键字段**（通过 `{{...}}` 占位符）
- 包含该 stage 对应的 **pitfalls** 约束
- 明确输出格式（Markdown 结构化文本，便于宿主 Agent 提取为 JSON）

**模板变量约定**：
- 来自直接输入：`{{character}}`, `{{text}}`, `{{audience}}`, `{{problem}}`, `{{length}}`
- 来自前序 stage：`{{hard_facts.source_text}}`, `{{micro_scene.selected_moment}}` 等（点号路径）

### 2. JSON Schema (`templates/schemas/stage_*.json`)

每个 schema 描述该 stage **预期输出**的结构化数据，用于：
- 宿主 Agent 明确知道要生成什么字段
- `validator.py` 做格式校验

**示例** `stage_01_setup.json`：
```json
{
  "type": "object",
  "required": ["character", "text", "audience", "problem", "length", "hard_facts"],
  "properties": {
    "character": { "type": "string" },
    "text": { "type": "string" },
    "audience": { "type": "string" },
    "problem": { "type": "string" },
    "length": { "type": "string" },
    "hard_facts": {
      "type": "object",
      "required": ["source_text", "time", "place", "institutional_context", "controversies"],
      "properties": {
        "source_text": { "type": "string" },
        "time": { "type": "string" },
        "place": { "type": "string" },
        "institutional_context": { "type": "string" },
        "controversies": { "type": "string" }
      }
    }
  }
}
```

其余 schema 定义：
- `stage_02_scene.json`：`micro_scene`（含 `selected_moment`, `actions`, `others_reaction`, `dramatic_tension`, `visual_elements`）
- `stage_03_dissect.json`：`keyword_card`（array of objects），`ancient_modern_bridge`（array of objects）
- `stage_04_compose.json`：`final_copy`（string），`emotional_arc`（object with 4 stages）
- `stage_05_review.json`：`final_review`（object with 5 boolean/string answers），`verdict`（string: PASS / NEEDS_REVISION）

### 3. 脚本库 (`scripts/lib/`)

#### `prompt_builder.py`
核心函数：
```python
def build_stage_prompt(stage: str, state: dict) -> str:
    """
    读取 templates/prompts/stage_{stage}.md，
    用 state 字典中的值替换所有 {{key}} 和 {{dot.path}} 占位符。
    如果某个占位符在 state 中找不到，保留原样或替换为空字符串。
    """
```

支持嵌套 dict 的点号路径解析（如 `{{hard_facts.time}}` → `state["hard_facts"]["time"]`）。

#### `validator.py`
核心函数：
```python
def validate_stage_output(stage: str, data: dict) -> list[str]:
    """
    用 templates/schemas/stage_{stage}.json 校验 data。
    返回错误信息列表（空列表表示通过）。
    """
```

依赖 `jsonschema`（可选，如果未安装则打印 warning 并跳过校验）。

#### `state.py`
核心函数：
```python
def load_state(path: str) -> dict: ...
def save_state(path: str, data: dict) -> None: ...
def merge_state(base: dict, overlay: dict) -> dict: ...
```

### 4. Orchestrator CLI (`scripts/shijing_agent.py`)

命令行接口（使用 `argparse` subparsers）：

```bash
# 运行单个 stage，输出生成的 prompt
python scripts/shijing_agent.py stage <stage_name> [options]

# 验证一个 JSON 文件是否符合对应 stage 的 schema
python scripts/shijing_agent.py validate --stage <stage_name> --input <json_file>

# 一键生成全 pipeline 的所有 prompts 到目录
python scripts/shijing_agent.py pipeline --config task.yaml --out-dir ./pipeline
```

#### `stage` subcommand 参数
```bash
python scripts/shijing_agent.py stage setup \
  --character 苏轼 --text 定风波 --audience 职场人 --problem 焦虑 --length 1200 \
  --output stage_01_prompt.md

python scripts/shijing_agent.py stage scene \
  --input stage_01_output.json \
  --output stage_02_prompt.md
```

实现逻辑：
1. 如果有 `--input`，读取 JSON 作为 base state
2. 如果有额外的 `--character` 等参数，覆盖到 state
3. 调用 `build_stage_prompt(stage, state)`
4. 输出 prompt 到 stdout 或 `--output` 文件

#### `pipeline` subcommand
读取 `--config` YAML（或直接用命令行参数），为 5 个 stage 分别生成 prompt 文件：
- `out-dir/stage_01_setup_prompt.md`
- `out-dir/stage_02_scene_prompt.md`
- ...以此类推

### 5. `SKILL.md` 更新

在现有内容基础上重构为：
- **Trigger**（不变）
- **Progressive Workflow**：说明为什么拆成 5 stage，以及宿主 Agent 如何使用
- **Stage Reference**：每个 stage 的输入、输出、关键约束一览表
- **Data Contract**：完整的状态 JSON 结构说明
- **Pitfalls**（不变）
- **Verification Checklist**（不变）

开头增加声明：
> 本 Skill 采用**渐进式工作流**，零 LLM API 依赖。它提供分阶段的 Prompt 模板与数据验证工具，由宿主 Agent 分次调用 LLM 完成创作。

### 6. `README.md` 更新

更新 Usage 章节，展示新的 CLI 用法。保留 bilingual 格式和 PM Standard 结构。

---

## 验收标准

- [ ] 5 个 stage 的 prompt 模板均独立存在且职责单一
- [ ] 5 个 JSON Schema 均存在且能覆盖各 stage 的输出结构
- [ ] `prompt_builder.py` 支持点号路径变量替换
- [ ] `validator.py` 能正确校验/报错
- [ ] `state.py` 能读写/合并 JSON 状态
- [ ] `shijing_agent.py` 的 `stage`, `validate`, `pipeline` 三个 subcommand 均可正常运行
- [ ] `python -m py_compile scripts/shijing_agent.py` 无语法错误
- [ ] `SKILL.md` 和 `README.md` 已更新为 v2.0 渐进式工作流说明
- [ ] 所有改动已 push 到 `origin main`

---

## 开发原则

- **不调 LLM API**：任何代码都不能包含 openai/anthropic/kimi 等调用
- **渐进式**：每个 stage prompt 尽量精简，只承载当前阶段必需的信息
- **数据驱动**：stage 间通过 JSON 文件传递状态，prompt 通过模板自动组装
