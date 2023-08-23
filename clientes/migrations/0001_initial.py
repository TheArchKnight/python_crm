# Generated by Django 4.2 on 2023-08-23 01:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_orgnanizacion', models.CharField(max_length=150)),
                ('direccion', models.CharField(max_length=255)),
                ('apartamentos', models.CharField(max_length=50)),
                ('nit', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254, null=True)),
                ('frecuencia_meses', models.IntegerField(default=1)),
                ('fecha_vencimiento', models.DateField(default=None, null=True)),
                ('administrador', models.CharField(max_length=150)),
                ('supervisor', models.CharField(max_length=50)),
                ('telefono_supervisor', models.CharField(max_length=30)),
                ('correo_supervisor', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=30)),
                ('estado', models.CharField(choices=[('INACTIVO', 'Inactivo'), ('POTENCIAL', 'Potencial')], max_length=20)),
                ('rechazos', models.IntegerField(default=0)),
                ('estado_servicio', models.CharField(choices=[('VENCIDO', 'Vencido'), ('GARANTIA', 'Garantia'), ('EN TERMINOS', 'En terminos')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('observaciones', models.CharField(max_length=255)),
                ('estado', models.CharField(choices=[('FINALIZADA', 'Finalizada'), ('EN PROCESO', 'En proceso'), ('PENDIENTE', 'Pendiente')], default='EN PROCESO', max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('empleado', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='Llamada',
            fields=[
                ('interaccion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clientes.interaccion')),
            ],
            bases=('clientes.interaccion',),
        ),
        migrations.CreateModel(
            name='Visita',
            fields=[
                ('interaccion_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='clientes.interaccion')),
            ],
            bases=('clientes.interaccion',),
        ),
        migrations.AddField(
            model_name='cliente',
            name='empleado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.empleado'),
        ),
    ]
