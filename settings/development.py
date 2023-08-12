from .base import *

SECRET_KEY = env('SECRET_KEY_DEV')
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
        "default": {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('DB_NAME_DEV'),
            'USER': env('DB_USER_DEV'),
            'PASSWORD': env('DB_PASSWORD_DEV'),
            'HOST':env('DB_HOST_DEV'),
            'PORT':env('DB_PORT_DEV'),
            }
        }
#TODO
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env('EMAIL_HOST_DEV')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER_DEV')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD_DEV')
#TODO
CELERY_RESULT_BACKEND = f"db+mysql://{env('DB_USER_DEV')}:{env('DB_PASSWORD_DEV')}@{env('DB_HOST_DEV')}/{env('DB_NAME_DEV')}?charset=utf8mb4"

