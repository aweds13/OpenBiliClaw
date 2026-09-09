"""Dedicated recommendation API process.

Uses a Unix domain socket on POSIX platforms.  Windows asyncio/uvicorn cannot
create Unix sockets, so the Windows build binds a loopback TCP port instead.
"""

from __future__ import annotations

import os

import uvicorn

from openbiliclaw.api.app import create_app
from openbiliclaw.config import load_config
from openbiliclaw.recommendation_runtime import (
    DEFAULT_RECOMMENDATION_PORT,
    RECOMMENDATION_PORT_ENV,
    RECOMMENDATION_SOCK_ENV,
    recommendation_sock_from_data_path,
)


def main() -> None:
    app = create_app()
    recommendation_port = os.environ.get(RECOMMENDATION_PORT_ENV, "").strip()
    if os.name == "nt" or recommendation_port:
        port = int(recommendation_port or str(DEFAULT_RECOMMENDATION_PORT))
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
        return

    sock = os.environ.get(RECOMMENDATION_SOCK_ENV)
    if not sock:
        sock = recommendation_sock_from_data_path(load_config().data_path)
    os.makedirs(os.path.dirname(sock), mode=0o700, exist_ok=True)
    uvicorn.run(app, uds=sock, log_level="info")


if __name__ == "__main__":
    main()
