# config/settings/production.py
from .base import *  # noqa: F403

# ---------------------------------------------------------------------------
# Override for production
# ---------------------------------------------------------------------------
DEBUG = False

# Use PostgreSQL with pgvector in production
# Set DATABASE_URL in the environment, e.g.:
#   postgres://user:pass@host:5432/marketing_os
# The pgvector extension is required for the vector store.

# Security hardening
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Only allow specific origins in production
CORS_ALLOW_ALL_ORIGINS = False

# Production static file serving
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
