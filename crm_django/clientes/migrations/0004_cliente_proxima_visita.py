# Generated by Django 4.1.5 on 2023-02-01 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0003_cliente_frecuencia_meses_cliente_ultima_visita"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="proxima_visita",
            field=models.DateField(null=True),
        ),
    ]
