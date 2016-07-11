INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'lsapling',
    'testapp',
)

SECRET_KEY = 'abc123'

try:
    from local_settings import *
except ImportError:
    pass
