#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
史镜 Agent CLI Tool

A command-line utility that generates structured input for the Shijing Agent
(historical empathy copywriting workflow) and formats the output into a
7-section report.

Sections:
    1. 硬事实卡 (Hard Facts Card)
    2. 微场景 (Micro Scene)
    3. 词眼卡 (Keyword Card)
    4. 古今对照卡 (Ancient-Modern Bridge Card)
    5. 情绪曲线 (Emotional Arc)
    6. 成稿 (Final Copy)
    7. 终审 (Final Review)
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def load_yaml_config(path: str) -> dict[str, Any]:
    """Load configuration from a YAML file."""
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to load YAML config files. "
            "Install it with: pip install pyyaml"
        ) from exc
    with open(path, "r", encoding="utf-8") as f:
        config_data = yaml.safe_load(f)
    if not isinstance(config_data, dict):
        raise ValueError("Config file must contain a YAML mapping (key-value pairs), got %s" % type(config_data).__name__)
    return config_data or {}


def build_prompt(params: dict[str, Any]) -> str:
    """Build the LLM prompt from template and parameters."""
    template_path = Path(__file__).parent.parent / "templates" / "prompt.md"
    if not template_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {template_path}")
    prompt = template_path.read_text(encoding="utf-8")
    prompt = prompt.replace("{{character}}", params.get("character", ""))
    prompt = prompt.replace("{{text}}", params.get("text", ""))
    prompt = prompt.replace("{{audience}}", params.get("audience", ""))
    prompt = prompt.replace("{{problem}}", params.get("problem", ""))
    prompt = prompt.replace("{{length}}", str(params.get("length", "")))
    return prompt


def build_markdown_report(params: dict[str, Any], prompt: str) -> str:
    """Build a structured markdown report for manual or LLM-assisted filling."""
    now = datetime.now().isoformat()
    lines = [
        "# 史镜 Agent 结构化报告",
        "",
        f"生成时间：{now}",
        "",
        "## 任务参数",
        "",
        f"- **人物**：{params.get('character', '')}",
        f"- **文本**：{params.get('text', '')}",
        f"- **受众**：{params.get('audience', '')}",
        f"- **困境**：{params.get('problem', '')}",
        f"- **字数**：{params.get('length', '')}",
        "",
        "---",
        "",
        "## 1. 硬事实卡",
        "",
        "原典：\n\n时间：\n\n地点：\n\n制度处境：\n\n争议点：",
        "",
        "## 2. 微场景",
        "",
        "选定的最小瞬间：\n\n具体动作：\n\n他人反应：\n\n戏剧张力：",
        "",
        "## 3. 词眼卡",
        "",
        "| 词眼 | 字面意思 | 现场动作 | 心理位移 | 现代映射 |",
        "| :--- | :--- | :--- | :--- | :--- |",
        "|  |  |  |  |  |",
        "",
        "## 4. 古今对照卡",
        "",
        "| 历史细节 | 现代问题 | 映射类型 |",
        "| :--- | :--- | :--- |",
        "|  |  | 系统映射 / 字面联想 |",
        "",
        "## 5. 情绪曲线",
        "",
        "- 压迫：\n- 对抗：\n- 停顿：\n- 翻转/回望：",
        "",
        "## 6. 成稿",
        "",
        "（此处填入按照\"困境→现场→拆句→对照→翻转→心法\"结构写成的文案）",
        "",
        "## 7. 终审（五问）",
        "",
        "1. 瞬间可见？\n   答：",
        "2. 坐标成立？\n   答：",
        "3. 回得去原文？\n   答：",
        "4. 系统同构？\n   答：",
        "5. 可执行心法？\n   答：",
        "",
        "---",
        "",
        "## 附录：Prompt",
        "",
        "```markdown",
        prompt,
        "```",
    ]
    return "\n".join(lines)


def build_json_report(params: dict[str, Any], prompt: str) -> dict[str, Any]:
    """Build a structured JSON report scaffold."""
    return {
        "meta": {
            "generated_at": datetime.now().isoformat(),
            "params": params,
        },
        "sections": {
            "hard_facts": {
                "source_text": "",
                "time": "",
                "place": "",
                "institutional_context": "",
                "controversies": "",
            },
            "micro_scene": {
                "selected_moment": "",
                "actions": "",
                "others_reaction": "",
                "dramatic_tension": "",
            },
            "keyword_card": [],
            "ancient_modern_bridge": [],
            "emotional_arc": {
                "oppression": "",
                "confrontation": "",
                "pause": "",
                "flip_or_retrospect": "",
            },
            "final_copy": "",
            "final_review": {
                "q1_visible_moment": "",
                "q2_coordinate_valid": "",
                "q3_back_to_source": "",
                "q4_structural_isomorphism": "",
                "q5_actionable_insight": "",
            },
        },
        "prompt": prompt,
    }


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="shijing-agent",
        description=(
            "史镜 Agent CLI — 为历史人物深描型情绪文案\n"
            "生成 7 步工作流的结构化输入与输出报告"
        ),
    )
    parser.add_argument(
        "--character",
        type=str,
        default="",
        help="历史人物名称（例：苏轼）",
    )
    parser.add_argument(
        "--text",
        type=str,
        default="",
        help="核心文本或事件（例：定风波）",
    )
    parser.add_argument(
        "--audience",
        type=str,
        default="",
        help="目标受众（例：25-35 岁职场人）",
    )
    parser.add_argument(
        "--problem",
        type=str,
        default="",
        help="当代情绪困境（例：失业焦虑）",
    )
    parser.add_argument(
        "--length",
        type=str,
        default="",
        help="成稿字数或时长（例：1200）",
    )
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="YAML 配置文件路径（可覆盖命令行参数）",
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["markdown", "json"],
        default="markdown",
        help="输出格式（默认 markdown）",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="输出文件路径（默认输出到 stdout）",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    params: dict[str, Any] = {
        "character": args.character,
        "text": args.text,
        "audience": args.audience,
        "problem": args.problem,
        "length": args.length,
    }

    if args.config:
        if not os.path.isfile(args.config):
            print(f"Error: config file not found: {args.config}", file=sys.stderr)
            return 1
        config_data = load_yaml_config(args.config)
        for key in params:
            if key in config_data and config_data[key] is not None:
                params[key] = config_data[key]

    missing = [k for k, v in params.items() if not v]
    if missing:
        print(
            f"Error: missing required parameters: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    try:
        prompt = build_prompt(params)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        report = build_json_report(params, prompt)
        content = json.dumps(report, ensure_ascii=False, indent=2)
    else:
        content = build_markdown_report(params, prompt)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"Report written to: {out_path}")
    else:
        print(content)

    return 0


if __name__ == "__main__":
    sys.exit(main())
