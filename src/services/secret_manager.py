"""
Secret Manager helper with safe fallbacks.

Usage:
    from src.services.secret_manager import load_secret_into_env
    load_secret_into_env("DATABASE_URL")

Behaviors:
    - Respects DISABLE_SECRET_MANAGER=true to fail-open without raising.
    - Uses GOOGLE_CLOUD_PROJECT or GCP_PROJECT to resolve project_id.
    - Secret id defaults to normalized env key (lowercase, underscores->dashes),
      but can be overridden via argument.
    - Returns the secret value (str) or None on failure.
"""

from __future__ import annotations

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def _get_project_id() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def _normalize_secret_id(env_key: str) -> str:
    return env_key.lower().replace("_", "-")


def fetch_secret(secret_id: str, project_id: Optional[str] = None, version: str = "latest") -> Optional[str]:
    """
    Fetch secret value from GCP Secret Manager.
    Returns None on any error (fail-open).
    """
    if os.getenv("DISABLE_SECRET_MANAGER", "false").lower() == "true":
        return None

    project = project_id or _get_project_id()
    if not project:
        logger.warning("Secret Manager disabled: project_id not set")
        return None

    try:
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project}/secrets/{secret_id}/versions/{version}"
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.warning(f"Secret Manager fetch failed for {secret_id}: {e}")
        return None


def load_secret_into_env(env_key: str, secret_id: Optional[str] = None, project_id: Optional[str] = None) -> Optional[str]:
    """
    If env var is missing, try to load from Secret Manager and set it.
    Returns the value (either pre-existing or fetched) or None.
    """
    current = os.getenv(env_key)
    if current:
        return current

    sid = secret_id or _normalize_secret_id(env_key)
    value = fetch_secret(sid, project_id=project_id)
    if value:
        os.environ[env_key] = value
        logger.info(f"Secret {env_key} loaded from Secret Manager (id={sid})")
    return value

