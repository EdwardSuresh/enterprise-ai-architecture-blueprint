"""Locate the kit repository and load YAML files from it."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def repo_root() -> Path:
    """Return the repo root: $KIT_ROOT, else the nearest parent holding kit.yaml."""
    env = os.environ.get("KIT_ROOT")
    if env:
        return Path(env).resolve()
    for start in (Path.cwd(), Path(__file__).resolve()):
        for parent in [start, *start.parents]:
            if (parent / "kit.yaml").is_file():
                return parent
    raise FileNotFoundError("kit.yaml not found. Run from the repo or set KIT_ROOT.")


def load_yaml(path: str | Path) -> Any:
    p = Path(path)
    if not p.is_absolute():
        p = repo_root() / p
    with p.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def kit_settings() -> dict:
    return load_yaml("kit.yaml")
