from __future__ import annotations

import asyncio
import os
from contextlib import suppress

import uvicorn

from api.app import app
from api.config import settings

if __name__ == "__main__":
    port = int(os.environ.get("PORT", settings.port))
    with suppress(KeyboardInterrupt, asyncio.CancelledError):
        uvicorn.run(app, host=settings.host, port=port, log_config=None, log_level=None)
