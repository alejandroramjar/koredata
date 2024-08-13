from base import *

SECRET_KEY = get_env_variable("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = get_env_variable("DJANGO_ALLOWED_HOSTS")
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_variable('DB_NAME'),
        'HOST': get_env_variable('DB_HOST'),
        'USER': get_env_variable('DB_USER'),
        'PASSWORD': get_env_variable('DB_PASSWORD'),
        'ATOMIC_REQUESTS': True,
    }
}

EMAIL_HOST = get_env_variable('EMAIL_HOST')
EMAIL_PORT = get_env_variable('EMAIL_PORT')
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = get_env_variable('EMAIL_USE_TLS')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# cookies
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 600  # 10 minutes only