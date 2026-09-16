#!/usr/bin/env python3
"""Ad-hoc structural verifier for redacted public Hermes backups."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml

PLACEHOLDER = "__REDACTED_FOR_GITHUB_BACKUP__"


def resolve(data: Any, dotted_path: str) -> Any:
    value = data
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise AssertionError(f"missing expected field: {dotted_path}")
        value = value[part]
    return value


def reject_malformed_placeholder_mappings(value: Any, path: str = "<root>") -> None:
    if isinstance(value, dict):
        if PLACEHOLDER in value:
            raise AssertionError(
                f"malformed redaction mapping at {path}; placeholder must be a scalar value"
            )
        for key, child in value.items():
            reject_malformed_placeholder_mappings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            reject_malformed_placeholder_mappings(child, f"{path}[{index}]")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config", type=Path)
    parser.add_argument(
        "--expect-placeholder",
        action="append",
        default=[],
        metavar="DOTTED_PATH",
        help="field that must equal the scalar redaction placeholder; repeatable",
    )
    args = parser.parse_args()

    with args.config.open(encoding="utf-8") as stream:
        config = yaml.safe_load(stream)

    if not isinstance(config, dict):
        raise AssertionError("config root must be a mapping")

    reject_malformed_placeholder_mappings(config)
    for dotted_path in args.expect_placeholder:
        value = resolve(config, dotted_path)
        if not isinstance(value, str) or value != PLACEHOLDER:
            raise AssertionError(
                f"{dotted_path} must be the scalar placeholder {PLACEHOLDER!r}"
            )

    print("PASS: YAML parses and redaction placeholders retain scalar structure")


if __name__ == "__main__":
    main()
