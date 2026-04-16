#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build stage prompts by replacing {{key}} and {{dot.path}} placeholders."""

import json
import re
from pathlib import Path


def _format_value(value) -> str:
    """Serialize lists/dicts as JSON; fall back to str for other types."""
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value) if value is not None else ""


def _resolve_dot_path(state: dict, path: str) -> str:
    """Resolve a dot-path like 'hard_facts.time' from a nested dict."""
    keys = path.strip().split(".")
    value = state
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return ""
    return _format_value(value)


def build_stage_prompt(stage: str, state: dict) -> str:
    """
    Read templates/prompts/stage_{stage}.md and replace all {{key}} and {{dot.path}}
    placeholders with values from state. If a placeholder is not found, replace with
    an empty string.
    """
    template_path = (
        Path(__file__).parent.parent.parent / "templates" / "prompts" / f"stage_{stage}.md"
    )
    if not template_path.exists():
        raise FileNotFoundError(f"Prompt template not found: {template_path}")

    prompt = template_path.read_text(encoding="utf-8")

    def replacer(match: "re.Match[str]") -> str:
        key = match.group(1).strip()
        if "." in key:
            return _resolve_dot_path(state, key)
        value = state.get(key)
        return _format_value(value)

    return re.sub(r"\{\{\s*([^}]+)\s*\}\}", replacer, prompt)
