from .base import *  # noqa: F403
from .base import env

DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
WHITENOISE_USE_FINDERS = True

if not DEBUG:
    raise RuntimeError("The local settings module requires DJANGO_DEBUG=true")
