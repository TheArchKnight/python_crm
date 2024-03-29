import environ
from pathlib import Path


from celery.schedules import crontab
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env()

environ.Env.read_env()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# Application definition

INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django_extensions",
        "django_celery_beat",
        "clientes",
        "empleados",
        "inventario",
        "fachadas",
        "general_usage",
#        "mensajes_masivos"
        ]

MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ]

ROOT_URLCONF = "crm_django.urls"

TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [BASE_DIR / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    ],
                },
            },
        ]

WSGI_APPLICATION = "crm_django.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
        {
            #   "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
            "NAME": "crm_django.validators.CustomAttributeSimilarityValidator"
            },
        {
            #    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
            "NAME" : "crm_django.validators.CustomMinimumLengthValidator"
            },
        {
            #        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
            "NAME": "crm_django.validators.CustomCommonPasswordValidator"
            },
        {
            #        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
            "NAME" : "crm_django.validators.CustomNumericPasswordValidator"
            },
        ]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "es-co"

TIME_ZONE = "America/Bogota"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/var/www/python_crm/static"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'clientes.User'


LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/"
LOGOUT_REDIRECT_URL = "/"
CELERY_BROKER_URL = "redis://localhost:6379"

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

CELERY_TIMEZONE = "America/Bogota"

CELERY_BEAT_SCHEDULE = { # scheduler configuration 
                        # "send_notifications" : {
                            #    "task" : "clientes.tasks.send_notifications",
                            #   "schedule" : crontab('0', '7', '1-5'),

                            #}
                        "garantias" : {
                            "task" : "clientes.tasks.llamadas",
                            "schedule" : crontab('0', '7', '1-5'),

                            },
                        "visitas": {
                            "task" : "clientes.tasks.visitas",
                            "schedule" : crontab('0', '7', '1-5'),

                            }
                        }


