# Generated by Django 4.1.5 on 2023-03-03 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0019_cliente_rechazos"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="fecha_llamada",
            field=models.DateField(default=None, null=True),
        ),
    ]
