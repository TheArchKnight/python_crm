# Generated by Django 4.1.7 on 2023-04-02 08:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0002_alter_elemento_fecha"),
        ("general_usage", "0007_alter_objeto_fecha"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="elemento",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="inventario.elemento",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="objeto",
            name="fecha",
            field=models.DateTimeField(
                default=datetime.datetime(2023, 4, 2, 3, 53, 45, 784398)
            ),
        ),
    ]
