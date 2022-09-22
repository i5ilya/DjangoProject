import os
from typing import Any

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()
from django.core.management import call_command
from products.models import Product, Folder

all_Folder = Folder.objects.all()
products = Product.objects.all()

diction = {}

for items in products:
    diction[items.folder_id] = items.name


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


# create_product(7231, 'Вино Кагор 150', 7234, 100)

tree_raw = Folder.dump_bulk()


# branch = Folder.dump_bulk(node_obj)
# print(all_Folder)

# create_folder(1, 'меню', 0, 1)

# (get_name(2).add_child(name='Wine'))  # добавить папочку в подпапку get_name(2)
# (get_name(2).add_child(name='Wine', id=345))  # добавить папочку в подпапку get_name(2)
def detour_tree(tree):
    print((tree['data'])['name'])
    tree_id = tree['id']
    for key, value in diction.items():
        if key == tree_id:
            print(value)
    # print((tree['id']))
    if tree.get('children'):
        for i in tree['children']:
            detour_tree(i)
    # else:
    # print((tree['data'])['name'])



print(tree_raw)
for it in tree_raw:
    detour_tree(it)




for product in products:

    print(product.name)