# Generated by Django 4.2 on 2023-04-13 22:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0004_cliente_correo_supervisor_cliente_supervisor_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="fumigacion",
            new_name="clientes",
        ),
    ]