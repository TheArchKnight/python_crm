from .base import *

SECRET_KEY = env('SECRET_KEY_PRODUCTION')
DEBUG = False
ALLOWED_HOSTS = ['192.168.0.119', '10.0.0.1']

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
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env('EMAIL_HOST_PRODUCTION')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER_PRODUCTION')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD_PRODUCTION')
CELERY_RESULT_BACKEND = f"db+mysql://{env('DB_USER_PRODUCTION')}:{env('DB_PASSWORD_PRODUCTION')}@{env('DB_HOST_PRODUCTION')}/{env('DB_NAME_PRODUCTION')}?charset=utf8mb4"

# Configuración de seguridad de cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuración de seguridad de autenticación
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]
# Configuración de seguridad de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}
