from .base import *  # noqa: F403

DEBUG = True
CORS_ALLOWED_ORIGINS = env.list(  # noqa: F405
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:5173", "http://localhost:3000"],
)
