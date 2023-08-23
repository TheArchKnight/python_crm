import multiprocessing

bind = '0.0.0.0:8000'
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
loglevel = 'info'

# Especifica el módulo de configuración de Django
env = 'DJANGO_SETTINGS_MODULE=settings.development'

