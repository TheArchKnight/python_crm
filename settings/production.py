from .base import *

SECRET_KEY = env('SECRET_KEY_PRODUCTION')
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME_PRODUCTION'),
            'USER': env('DB_USER_PRODUCTION'),
            'PASSWORD': env('DB_PASSWORD_PRODUCTION'),
            'HOST':env('DB_HOST_PRODUCTION'),
            'PORT':env('DB_PORT_PRODUCTION'),
            }
        }
#TODO
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env('EMAIL_HOST_PRODUCTION')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER_PRODUCTION')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD_PRODUCTION')
#TODO
CELERY_RESULT_BACKEND = f"db+mysql://{env('DB_USER_PRODUCTION')}:{env('DB_PASSWORD_PRODUCTION')}@{env('DB_HOST_PRODUCTION')}/{env('DB_NAME_PRODUCTION')}?charset=utf8mb4"

