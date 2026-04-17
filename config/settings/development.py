from .base import *

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')

CORS_ALLOW_ALL_ORIGINS = True
