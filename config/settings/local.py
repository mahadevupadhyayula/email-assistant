import os

from .base import *  # noqa: F403
from .base import env

DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
WHITENOISE_USE_FINDERS = True

if not DEBUG:
    raise RuntimeError("The local settings module requires DJANGO_DEBUG=true")

# OAuthLib otherwise rejects the documented localhost HTTP callback. This setting
# exists only in the local settings module and must never be copied to hosted config.
os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")
