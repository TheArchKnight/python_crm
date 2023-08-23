# Generated by Django 4.2 on 2023-08-23 01:27

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_obra', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=30)),
                ('nit', models.IntegerField()),
                ('administrador', models.CharField(max_length=30)),
                ('numero_tel', models.IntegerField()),
                ('correo', models.EmailField(max_length=254, null=True)),
                ('estado', models.CharField(choices=[('EN PROCESO', 'En proceso'), ('FINALIZADA', 'Finalizada')], max_length=10)),
                ('fecha_inicio', models.DateField(default=datetime.date.today)),
                ('costo_total', models.FloatField(default=0)),
                ('fecha_ultimo_pago', models.CharField(default=0, max_length=25)),
                ('empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('cargo', models.CharField(choices=[('SUPERVISOR', 'Supervisor'), ('OBRERO', 'Obrero')], max_length=30)),
                ('acumulado', models.FloatField(default=0)),
                ('obra', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fachadas.obra')),
            ],
        ),
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('periodo_inicio', models.DateField()),
                ('periodo_final', models.DateField()),
                ('monto', models.FloatField()),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fachadas.obra')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fachadas.trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Costo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=30)),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('precio_unidad', models.FloatField()),
                ('cobro_unidad', models.FloatField()),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fachadas.obra')),
            ],
        ),
        migrations.CreateModel(
            name='Accion',
            fields=[
                ('costo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='fachadas.costo')),
                ('trabajador', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fachadas.trabajador')),
            ],
            bases=('fachadas.costo',),
        ),
    ]
