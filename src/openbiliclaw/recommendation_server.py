"""Dedicated recommendation API process.

Runs a separate FastAPI instance on a Unix domain socket (default
``<data_path>/runtime/recommendation.sock``). The main API (8420) proxies only
recommendation routes to this socket, so recommendation serving gets its own
event loop / process without exposing another TCP port to clients.
"""

from __future__ import annotations

import os

import uvicorn

from openbiliclaw.api.app import create_app
from openbiliclaw.config import load_config


def main() -> None:
    sock = os.environ.get("OPENBILICLAW_RECOMMENDATION_SOCK")
    if not sock:
        sock = str(load_config().data_path / "runtime" / "recommendation.sock")
    sock_path = os.path.dirname(sock)
    os.makedirs(sock_path, mode=0o700, exist_ok=True)
    app = create_app()
    uvicorn.run(app, uds=sock, log_level="info")


if __name__ == "__main__":
    main()
