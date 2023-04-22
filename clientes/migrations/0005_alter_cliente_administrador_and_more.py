# Generated by Django 4.2 on 2023-04-22 03:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0004_alter_cliente_frecuencia_meses"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="administrador",
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name="cliente",
            name="frecuencia_meses",
            field=models.IntegerField(default=1),
        ),
    ]
