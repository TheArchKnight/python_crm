# Generated by Django 4.1.5 on 2023-03-08 22:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Llamada",
            fields=[
                (
                    "interaccion_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="clientes.interaccion",
                    ),
                ),
                (
                    "estado",
                    models.CharField(
                        choices=[
                            ("REALIZADA", "Realizada"),
                            ("PENDIENTE", "Pendiente"),
                        ],
                        default="PENDIENTE",
                        max_length=15,
                    ),
                ),
            ],
            bases=("clientes.interaccion",),
        ),
    ]
