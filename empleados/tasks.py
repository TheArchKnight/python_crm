from crm_django.celery import  app
from celery.schedules import crontab


@app.task
def add():
    return "Hello world!"
