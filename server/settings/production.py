# flake8: noqa


import dj_database_url
import server
from .base import *

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True


MIDDLEWARE_CLASSES = ('whitenoise.middleware.WhiteNoiseMiddleware',)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.append("whitenoise.middleware.WhiteNoiseMiddleware")

prod_db = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)

# ==============================================================================
# THIRD-PARTY APPS SETTINGS
# ==============================================================================
'''
sentry_sdk.init(
    dsn=config("SENTRY_DSN", default=""),
    environment=SERVER_ENVIRONMENT,
    release="server@%s" % server.__version__,
    integrations=[DjangoIntegration()],
) '''
