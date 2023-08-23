import os

from general_usage.models import Archivo

def write_file(files, path, user,model=None):
    file = None
    try:
        for f in files:
            with open(f"{path}/{f.name}", "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            file = Archivo.objects.create(ubicacion=model, nombre=f.name, usuario=user)      
    except FileNotFoundError:
        create_folder(path)
        file = write_file(files, path, user,model)
    return file

        
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

def filter_models(models, queryset):
    #Two arrays need to be passed, one with the model Classes to search and replace 
    #on the queryset. The queryset needs to be ordered
    lista_queryset = []
    for i in queryset:
        for j in models:
            try:
                elemento = j.objects.get(id=i.id)
                dict_queryset = {"elemento":elemento, "tipo":type(elemento).__name__}
                lista_queryset.append(dict_queryset)
                break
            except:
                continue
    return lista_queryset








