# Generated by Django 4.2 on 2023-10-21 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0006_interaccion_fecha_creacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empleado',
            name='organisation',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
