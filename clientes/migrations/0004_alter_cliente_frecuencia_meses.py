# Generated by Django 4.2 on 2023-04-22 03:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0003_alter_cliente_nombre_orgnanizacion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="frecuencia_meses",
            field=models.IntegerField(default=1, null=True),
        ),
    ]