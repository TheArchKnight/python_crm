# Generated by Django 4.1.5 on 2023-01-30 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cliente",
            name="administrador",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="frecuencia_meses",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="n_aptos",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="observaciones",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="proxima_visita",
        ),
        migrations.RemoveField(
            model_name="cliente",
            name="ultima_visita",
        ),
    ]