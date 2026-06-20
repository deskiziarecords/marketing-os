# config/settings/local.py
from .base import *  # noqa: F403

# ---------------------------------------------------------------------------
# Override for local development
# ---------------------------------------------------------------------------
DEBUG = True

# Use SQLite for quick local dev (override DATABASE_URL in .env for Postgres)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

# Show emails in the console instead of sending them
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Allow all origins in dev
CORS_ALLOW_ALL_ORIGINS = True

# Disable password strength checks in dev
AUTH_PASSWORD_VALIDATORS = []
