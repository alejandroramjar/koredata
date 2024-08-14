from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='koredata'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
# ALLOWED_HOSTS = ["127.0.0.1"]
# ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = [f'127.0.0.{i}' for i in range(1, 256)]
CORS_ALLOW_ALL_ORIGINS = True

# ***********************CONFIG EMAIL********************************************
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'koredatatesting@gmail.com'  # koredatatesting@gmail.com
EMAIL_HOST_PASSWORD = 'audj ucrj qlbk xmon'  # audj ucrj qlbk xmon
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_EMAIL = 'ramjar2107@gmail.com'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# *********************** END CONFIG EMAIL***************************************

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['file', 'console'],  # se quito la consola del registro de eventos
        'level': 'DEBUG',
        'propagate': True,
    },
    'loggers': {
        'django': {
            'handlers': ['file'],  # se quito la consola del registro de eventos
            'level': 'DEBUG',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['file'],  # se quito la consola del registro de eventos
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
