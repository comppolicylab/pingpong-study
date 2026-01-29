import logging
import time
from contextlib import asynccontextmanager
from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.responses import JSONResponse

import pingpong.metrics as metrics
from .config import config
from .errors import sentry

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run services in the background."""
    with sentry(), metrics.metrics():
        yield


app = FastAPI(
    lifespan=lifespan,
    openapi_url=None,
    docs_url=None,
    redoc_url=None,
    swagger_ui_oauth2_redirect_url=None,
)


@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    """Handle exceptions."""
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error."},
        )


# Conditionally mount Study app when configured
try:
    if config.study_public_url and config.study:
        from pingpong.study.server import study as study_app

        # Attach logging middleware to study app
        @study_app.middleware("http")
        async def log_request(request: Request, call_next):
            """Log the request."""
            metrics.in_flight.inc(app=config.study_public_url)
            start_time = time.monotonic()
            result = None
            try:
                result = await call_next(request)
                return result
            finally:
                metrics.in_flight.dec(app=config.study_public_url)
                status = result.status_code if result else 500
                duration = time.monotonic() - start_time
                metrics.api_requests.inc(
                    app=config.study_public_url,
                    route=request.url.path,
                    method=request.method,
                    status=status,
                )
                metrics.api_request_duration.observe(
                    duration,
                    app=config.study_public_url,
                    route=request.url.path,
                    method=request.method,
                    status=status,
                )
                if config.development:
                    logger.debug(
                        "Request %s %s %s %s",
                        request.method,
                        request.url.path,
                        status,
                        duration,
                    )

        app.mount("/api/study", study_app)
except Exception:
    # If study is not configured or import fails, skip mounting
    logger.exception("Failed to mount study app.")
    pass


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok"}
