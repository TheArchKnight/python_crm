import os

from general_usage.models import Archivo

def write_file(files, path, model, user):
    try:
        for f in files:
            with open(f"{path}/{f.name}", "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            Archivo.objects.create(ubicacion=model, nombre=f.name, usuario=user)
    except FileNotFoundError:
        create_folder(path)
        write_file(files, path)
        
def create_folder(full_path):
    list_path = full_path.split("/")
    path = "/"
    for i in range(len(list_path)):
        if list_path[i] != '':
            path += list_path[i] + "/"
            try:
                os.mkdir(path)
            except FileExistsError:
                continue





