"""Dedicated recommendation API process.

Runs a separate FastAPI instance on ``OPENBILICLAW_RECOMMENDATION_PORT``
(default 8422). The main API (8420) proxies only recommendation routes here,
so heavy recommendation work gets its own event loop / process and does not
compete with chat, messages, or status endpoints.
"""

from __future__ import annotations

import os

import uvicorn

from openbiliclaw.api.app import create_app


def main() -> None:
    host = os.environ.get("OPENBILICLAW_RECOMMENDATION_HOST", "127.0.0.1")
    port = int(os.environ.get("OPENBILICLAW_RECOMMENDATION_PORT", "8422"))
    app = create_app()
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
