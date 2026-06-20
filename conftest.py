# Root conftest — runs before any plugin or test conftest.
# On Windows, psycopg[binary] bundles OpenSSL DLLs that conflict with the
# cryptography package's Rust extension (_rust.pyd). Importing ssl first
# registers the APPLINK function pointers before either library loads OpenSSL.
import ssl  # noqa: F401
try:
    import psycopg  # noqa: F401 — loads psycopg's OpenSSL DLLs early, before cryptography
except ImportError:
    pass
