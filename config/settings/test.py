import environ
from .base import *

env = environ.Env(DEBUG=(bool,False))
environ.Env.read_env(os.path.join(BASE_DIR,'.env'))

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS',default=[])

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS',default=[])
