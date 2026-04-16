#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
史镜 Agent CLI Tool v2.0

Orchestrator for the progressive 5-stage Shijing Agent workflow.
Zero LLM API dependency.

Subcommands:
    stage      Build a prompt for a single stage
    validate   Validate a JSON file against a stage schema
    pipeline   Generate all 5 stage prompts in one shot
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

from lib.prompt_builder import build_stage_prompt
from lib.state import load_state, merge_state, save_state
from lib.validator import validate_stage_output


STAGE_NAMES = ["01_setup", "02_scene", "03_dissect", "04_compose", "05_review"]


def _load_yaml_config(path: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "PyYAML is required to load YAML config files. "
            "Install it with: pip install pyyaml"
        ) from exc
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"Config file must contain a YAML mapping, got {type(data).__name__}")
    return data


def _build_base_state(args: argparse.Namespace) -> dict[str, Any]:
    """Build state from --input, --config, and direct CLI args."""
    state: dict[str, Any] = {}

    if getattr(args, "input", None):
        state = load_state(args.input)

    if getattr(args, "config", None):
        if not os.path.isfile(args.config):
            print(f"Error: config file not found: {args.config}", file=sys.stderr)
            sys.exit(1)
        config_data = _load_yaml_config(args.config)
        state = merge_state(state, config_data)

    # Direct overrides
    for key in ("character", "text", "audience", "problem", "length"):
        if hasattr(args, key):
            value = getattr(args, key)
            if value:
                state[key] = value

    return state


def _cmd_stage(args: argparse.Namespace) -> int:
    stage = args.stage_name
    state = _build_base_state(args)

    try:
        prompt = build_stage_prompt(stage, state)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(prompt, encoding="utf-8")
        print(f"Prompt written to: {out_path}")
    else:
        print(prompt)

    return 0


def _cmd_validate(args: argparse.Namespace) -> int:
    stage = args.stage
    input_path = args.input
    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        data = load_state(input_path)
    except json.JSONDecodeError as exc:
        print(f"Error: JSON decode error: {exc}", file=sys.stderr)
        return 1

    errors = validate_stage_output(stage, data)
    if errors:
        print(f"Validation failed for stage '{stage}':")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"Validation passed for stage '{stage}'.")
    return 0


def _cmd_pipeline(args: argparse.Namespace) -> int:
    state: dict[str, Any] = {}
    if args.config:
        if not os.path.isfile(args.config):
            print(f"Error: config file not found: {args.config}", file=sys.stderr)
            return 1
        state = _load_yaml_config(args.config)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for stage in STAGE_NAMES:
        try:
            prompt = build_stage_prompt(stage, state)
        except FileNotFoundError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 1
        out_path = out_dir / f"{stage}_prompt.md"
        out_path.write_text(prompt, encoding="utf-8")
        print(f"Generated: {out_path}")

    return 0


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--character", type=str, default="", help="历史人物名称")
    parser.add_argument("--text", type=str, default="", help="核心文本或事件")
    parser.add_argument("--audience", type=str, default="", help="目标受众")
    parser.add_argument("--problem", type=str, default="", help="当代情绪困境")
    parser.add_argument("--length", type=str, default="", help="成稿字数或时长")
    parser.add_argument("--config", type=str, default=None, help="YAML 配置文件路径")
    parser.add_argument("--input", type=str, default=None, help="基础状态 JSON 文件路径")
    parser.add_argument("--output", type=str, default=None, help="输出文件路径（默认 stdout）")


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="shijing-agent",
        description="史镜 Agent CLI v2.0 — 渐进式 5-Stage 工作流编排与验证工具",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # stage subcommand
    stage_parser = subparsers.add_parser("stage", help="生成单个 stage 的 prompt")
    stage_parser.add_argument(
        "stage_name",
        choices=STAGE_NAMES,
        help="Stage 名称",
    )
    _add_common_args(stage_parser)
    stage_parser.set_defaults(func=_cmd_stage)

    # validate subcommand
    validate_parser = subparsers.add_parser("validate", help="验证 JSON 是否符合 stage schema")
    validate_parser.add_argument("--stage", required=True, choices=STAGE_NAMES, help="Stage 名称")
    validate_parser.add_argument("--input", required=True, help="待验证的 JSON 文件路径")
    validate_parser.set_defaults(func=_cmd_validate)

    # pipeline subcommand
    pipeline_parser = subparsers.add_parser("pipeline", help="一键生成全部 5 个 stage 的 prompts")
    pipeline_parser.add_argument("--config", required=True, help="YAML 配置文件路径")
    pipeline_parser.add_argument("--out-dir", required=True, help="输出目录")
    pipeline_parser.set_defaults(func=_cmd_pipeline)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
