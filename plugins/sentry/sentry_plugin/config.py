"""Environment configuration for the sentry integration (Phase 1)."""

from __future__ import annotations

import os
from typing import Any

GATE_ENV_VARS: tuple[str, ...] = ['SENTRY_AUTH_TOKEN']

INJECT_ENV_MAP: dict[str, str] = {'sentry_token': 'SENTRY_AUTH_TOKEN', 'organization_slug': 'SENTRY_ORG_SLUG', 'sentry_url': 'SENTRY_URL', 'project_slug': 'SENTRY_PROJECT_SLUG'}


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
