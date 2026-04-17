import environ
from .base import *

env = environ.Env(DEBUG=(bool,False))
environ.Env.read_env(os.path.join(BASE_DIR,'.env'))


DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS',default=[])

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS',default=[])

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True