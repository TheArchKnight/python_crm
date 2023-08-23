#!/bin/bash
redis-server &
sleep 2
export DJANGO_SETTINGS_MODULE=settings.development
python manage.py runserver --settings=settings.development &
sleep 2
celery -A crm_django worker -l info &
# Iniciar Celery beat en segundo plano
celery -A crm_django beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler & 
sleep 4
# Mostrar mensaje de que todo está listo
echo "Todos los servicios están en ejecución"

# Esperar a que se presione Ctrl+C para detener los servicios
trap 'kill $(jobs -p)' SIGINT SIGTERM EXIT
wait
