"""Shared runtime helpers for the dedicated recommendation API process.

On POSIX systems the recommendation process is exposed through a Unix domain
socket.  Windows asyncio/uvicorn does not implement ``create_unix_server``, so
on Windows the same process listens on a loopback TCP port instead.
"""

from __future__ import annotations

import os
from pathlib import Path

DEFAULT_RECOMMENDATION_PORT = 8423
RECOMMENDATION_SOCK_ENV = "OPENBILICLAW_RECOMMENDATION_SOCK"
RECOMMENDATION_PORT_ENV = "OPENBILICLAW_RECOMMENDATION_PORT"


def recommendation_sock_from_data_path(data_path: Path) -> str:
    """Return the default Unix socket path for a data directory."""
    return str(Path(data_path) / "runtime" / "recommendation.sock")


def ensure_recommendation_transport_env(data_path: Path) -> str:
    """Set the platform-appropriate recommendation transport environment.

    Returns a human-readable transport description for status/log output.
    """
    if os.name == "nt" or os.environ.get(RECOMMENDATION_PORT_ENV, "").strip():
        os.environ.setdefault(RECOMMENDATION_PORT_ENV, str(DEFAULT_RECOMMENDATION_PORT))
        os.environ.pop(RECOMMENDATION_SOCK_ENV, None)
        port = os.environ[RECOMMENDATION_PORT_ENV]
        return f"TCP 127.0.0.1:{port}"
    os.environ.setdefault(
        RECOMMENDATION_SOCK_ENV, recommendation_sock_from_data_path(data_path)
    )
    os.environ.pop(RECOMMENDATION_PORT_ENV, None)
    return f"Unix socket {os.environ[RECOMMENDATION_SOCK_ENV]}"


def recommendation_transport_enabled() -> bool:
    """Whether the main API is expected to proxy to a recommendation process."""
    return bool(
        os.environ.get(RECOMMENDATION_SOCK_ENV, "").strip()
        or os.environ.get(RECOMMENDATION_PORT_ENV, "").strip()
    )
