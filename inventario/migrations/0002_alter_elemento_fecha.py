# Generated by Django 4.1.7 on 2023-04-02 08:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventario", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="elemento",
            name="fecha",
            field=models.DateField(default=datetime.date(2023, 4, 2)),
        ),
    ]