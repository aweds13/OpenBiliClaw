"""Dedicated recommendation API process (Unix socket)."""

from __future__ import annotations

import os

import uvicorn

from openbiliclaw.api.app import create_app
from openbiliclaw.config import load_config


def main() -> None:
    sock = os.environ.get("OPENBILICLAW_RECOMMENDATION_SOCK")
    if not sock:
        sock = str(load_config().data_path / "runtime" / "recommendation.sock")
    os.makedirs(os.path.dirname(sock), mode=0o700, exist_ok=True)
    app = create_app()
    uvicorn.run(app, uds=sock, log_level="info")


if __name__ == "__main__":
    main()
