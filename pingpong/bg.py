import contextlib
import logging
import threading
import time
import uvicorn

from fastapi import FastAPI
from typing import Generator

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
def root() -> None:
    """Root endpoint."""
    return None


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}


class BackgroundServer(uvicorn.Server):
    """A uvicorn server that can be run in a background thread."""

    @contextlib.contextmanager
    def run_in_thread(self) -> Generator:
        start = time.monotonic()
        startup_timeout_s = 10.0
        shutdown_timeout_s = 5.0
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        try:
            while not self.started:
                if not thread.is_alive():
                    raise RuntimeError(
                        "Uvicorn server thread exited before startup completed."
                    )
                if time.monotonic() - start > startup_timeout_s:
                    raise TimeoutError("Uvicorn server startup timed out.")
                time.sleep(0.001)
            yield
        finally:
            self.should_exit = True
            thread.join(timeout=shutdown_timeout_s)
            if thread.is_alive():
                logger.warning(
                    "Uvicorn server thread did not stop within %.1f seconds.",
                    shutdown_timeout_s,
                )


def get_server(host="localhost", port=8001) -> BackgroundServer:
    """Get the background server."""
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    return BackgroundServer(config)
