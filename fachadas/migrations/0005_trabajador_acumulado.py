# Generated by Django 4.1.5 on 2023-03-22 20:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fachadas", "0004_alter_obra_fecha_inicio_trabajador_costo_accion"),
    ]

    operations = [
        migrations.AddField(
            model_name="trabajador",
            name="acumulado",
            field=models.FloatField(default=0),
        ),
    ]
