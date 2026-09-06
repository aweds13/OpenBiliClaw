"""Background discovery/runtime worker.

Builds the same runtime components as the main API, but instead of serving
HTTP it only runs ``ContinuousRefreshController.run_forever()``. This keeps
discovery / eval / producers / cover prefetch away from the main API event
loop while still letting the API stay fast for recommendations and chat.
"""

from __future__ import annotations

import asyncio
import os

from openbiliclaw.api.app import create_app


def main() -> None:
    os.environ.setdefault("OPENBILICLAW_FULL_WORKER", "1")
    app = create_app()
    ctx = getattr(app.state, "runtime_context", None)
    controller = getattr(ctx, "runtime_controller", None)
    run_forever = getattr(controller, "run_forever", None)
    if run_forever is None:
        raise RuntimeError("runtime_controller.run_forever not available")
    asyncio.run(run_forever())


if __name__ == "__main__":
    main()
