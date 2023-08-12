import pandas as pd
import os

# Configurar el entorno de Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.production'
import django
django.setup()
from clientes.models import Cliente

# Leer el archivo CSV
df = pd.read_csv('./data.csv')

df.fillna(value=0, inplace=True)
# Iterar a través de las filas del archivo CSV
for index, row in df.iterrows():
    # Crear y guardar un objeto Cliente
    obj = Cliente(nombre_orgnanizacion=row['NOMBRE_EDIFICIO'],
                  direccion=row[df.columns[2]],
                  apartamentos=row['APTOS'],
                  administrador=row['ADMINISTRADOR'],
                  telefono=row['NÚMERO CONTACTO'],
                  correo=row['CORREO ELECTRÓNICO'],
                  estado=row['ESTADO'],
                  frecuencia_meses=row['FRECUENCIA']
                  )
    obj.save()

print('Migración de datos completada con éxito!')

