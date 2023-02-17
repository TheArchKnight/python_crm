#!/bin/bash
source env/bin/activate
redis-server & python -m celery -A crm_django worker -l info & celery -A crm_django beat -l info & python manage.py runserver 
