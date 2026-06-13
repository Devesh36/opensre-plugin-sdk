"""Environment configuration for the mongodb_atlas integration (Phase 1)."""

from __future__ import annotations

import os
from typing import Any

GATE_ENV_VARS: tuple[str, ...] = ['MONGODB_ATLAS_PUBLIC_KEY']

INJECT_ENV_MAP: dict[str, str] = {'public_key': 'MONGODB_ATLAS_PUBLIC_KEY', 'private_key': 'MONGODB_ATLAS_PRIVATE_KEY', 'project_id': 'MONGODB_ATLAS_PROJECT_ID'}


def is_configured() -> bool:
    if not GATE_ENV_VARS:
        return True
    return any(os.environ.get(name, "").strip() for name in GATE_ENV_VARS)


def extract_env_params() -> dict[str, Any]:
    return {
        param: os.environ.get(env_name, "")
        for param, env_name in INJECT_ENV_MAP.items()
    }


def _available(sources: dict[str, dict]) -> bool:
    _ = sources
    return is_configured()


def _extract_params(sources: dict[str, dict]) -> dict[str, Any]:
    _ = sources
    return extract_env_params()
