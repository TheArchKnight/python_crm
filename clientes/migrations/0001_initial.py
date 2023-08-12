# Generated by Django 4.2 on 2023-04-14 16:23

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_organisor', models.BooleanField(default=False)),
                ('clientes', models.BooleanField(default=False)),
                ('inventario', models.BooleanField(default=False)),
                ('fachadas', models.BooleanField(default=False)),
                ('mensajes', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_orgnanizacion', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=255)),
                ('nit', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254, null=True)),
                ('frecuencia_meses', models.IntegerField(default=1)),
                ('fecha_vencimiento', models.DateField(default=None, null=True)),
                ('administrador', models.CharField(max_length=30)),
                ('supervisor', models.CharField(max_length=30)),
                ('telefono_supervisor', models.CharField(max_length=15)),
                ('correo_supervisor', models.EmailField(max_length=254)),
                ('telefono', models.CharField(max_length=10)),
                ('estado', models.CharField(choices=[('INACTIVO', 'Inactivo'), ('POTENCIAL', 'Potencial')], max_length=10)),
                ('rechazos', models.IntegerField(default=0)),
                ('estado_servicio', models.CharField(choices=[('VENCIDO', 'Vencido'), ('GARANTIA', 'Garantia'), ('EN TERMINOS', 'En terminos')], max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='empleado',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.userprofile'),
        ),
        migrations.AddField(
            model_name='empleado',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cliente',
            name='empleado',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.empleado'),
        ),
    ]
