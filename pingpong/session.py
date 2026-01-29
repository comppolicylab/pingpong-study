from fastapi import Request
from .now import NowFn, utcnow

import logging

logger = logging.getLogger(__name__)


def get_now_fn(req: Request) -> NowFn:
    """Get the current time function for the request."""
    return getattr(req.app.state, "now", utcnow)
