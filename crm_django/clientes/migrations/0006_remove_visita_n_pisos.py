# Generated by Django 4.1.5 on 2023-02-01 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0005_visita"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="visita",
            name="n_pisos",
        ),
    ]