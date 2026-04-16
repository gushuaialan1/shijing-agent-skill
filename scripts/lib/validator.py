#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate stage outputs against JSON schemas."""

import json
import warnings
from pathlib import Path


def validate_stage_output(stage: str, data: dict) -> list[str]:
    """
    Validate data against templates/schemas/stage_{stage}.json.
    Returns a list of error messages (empty list means valid).
    """
    schema_path = (
        Path(__file__).parent.parent.parent / "templates" / "schemas" / f"stage_{stage}.json"
    )
    if not schema_path.exists():
        return [f"Schema not found: {schema_path}"]

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Schema JSON decode error: {exc}"]

    try:
        import jsonschema  # type: ignore
    except ImportError:  # pragma: no cover
        warnings.warn(
            "jsonschema is not installed; skipping schema validation. "
            "Install it with: pip install jsonschema",
            stacklevel=2,
        )
        return []

    errors: list[str] = []
    validator = jsonschema.Draft7Validator(schema)
    for error in validator.iter_errors(data):
        path = "/".join(str(p) for p in error.path) if error.path else "<root>"
        errors.append(f"[{path}] {error.message}")
    return errors
