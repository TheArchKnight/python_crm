#!/bin/bash
source env/bin/activate
redis-server & python -m celery -A crm_django worker -l info & sleep 2s 
python manage.py runserver & celery -A crm_django beat -l info 
