from .base import *  # noqa

DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_ROOT = ''

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'phr', 'static')]  # NOQA
