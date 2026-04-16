#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read, write, and merge stage state JSON files."""

import json
from pathlib import Path


def load_state(path: str) -> dict:
    """Load state from a JSON file. Returns an empty dict if the file does not exist."""
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(path: str, data: dict) -> None:
    """Save state to a JSON file, creating parent directories if needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def merge_state(base: dict, overlay: dict) -> dict:
    """Deep-merge overlay into base. Returns a new dict without mutating inputs."""
    result = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            result[key] = merge_state(result[key], value)
        else:
            result[key] = value
    return result
