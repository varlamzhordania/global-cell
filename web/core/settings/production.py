import os

from .settings import *

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

CACHES = {
    'default': {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        'LOCATION': os.getenv("REDIS_HOST"),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_password")
