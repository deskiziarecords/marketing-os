# config/settings/test.py
from .local import *  # noqa: F403

# Exclude stripe/djstripe from tests — dj-stripe imports the stripe C extension
# which loads a conflicting OpenSSL DLL on Windows and crashes the test runner.
# Stripe functionality is integration-tested separately.
INSTALLED_APPS = [a for a in INSTALLED_APPS if a != "djstripe"]  # noqa: F405

# Disable Stripe settings to avoid validation errors without djstripe
STRIPE_LIVE_SECRET_KEY = "sk_test_dummy"
STRIPE_TEST_SECRET_KEY = "sk_test_dummy"
