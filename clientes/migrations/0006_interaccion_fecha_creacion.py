# Generated by Django 4.2 on 2023-10-20 23:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0005_alter_cliente_administrador_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaccion',
            name='fecha_creacion',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
