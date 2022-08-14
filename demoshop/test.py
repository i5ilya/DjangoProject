import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demoshop.settings")
import django
django.setup()
from django.core.management import call_command
from products.models import Product, Folder

all_Folder = Folder.objects.all()
all_Products = Product.objects.all()


def get_name(id):
    return Folder.objects.get(id=id)


def get_id(name):
    return Folder.objects.get(name=name)


def create_folder(id, name, parent_id, depth):
    '''
    :param id: "ID" servio
    :param name: "Name" servio
    :param parentid: "ParentID" - root folder
    :param depth: "HierarchyLevel"  == 1 for MENU (identical for Django DB)
    :return: do writing folders in DB
    '''
    if parent_id == 0 and depth == 1:  # в сервио parentid == 0 - это корневая папка и глубина ее == 1
        pass  # должна быть создана в БД с кодом сервио и мы ее не обрабатываем
    else:
        get_name(parent_id).add_child(id=id, name=name, depth=depth)  # в остальных случаях создаем папки в иерархии


def create_product(id, name, folder_id, price):
    '''
    :param id: "ID" Servio
    :param name: "Name" Servio
    :param folder_id: "ParentID" Servio
    :param price: "Price" Servio
    :return: do writing new product in DB
    '''
    new_product = Product(id=id, folder=Folder.objects.get(id=folder_id), name=name, price=price)
    new_product.save()


#create_product(7231, 'Вино Кагор 150', 7234, 100)

# create_folder(1, 'меню', 0, 1)

# (get_name(2).add_child(name='Wine'))  # добавить папочку в подпапку get_name(2)
# (get_name(2).add_child(name='Wine', id=345))  # добавить папочку в подпапку get_name(2)
# for items in all_Folder:
#     print(items.name)
#     print(items.id)

for items in all_Products:
    print(items.name)
    print(items.price)
    print(items.folder)
