# Generated by Django 4.1.5 on 2023-02-18 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0014_empleado_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="cliente",
            name="estado",
            field=models.CharField(
                choices=[
                    ("ACTIVO", "Activo"),
                    ("INACTIVO", "Inactivo"),
                    ("POTENCIAL", "Potencial"),
                ],
                default="ACTIVO",
                max_length=10,
            ),
            preserve_default=False,
        ),
    ]