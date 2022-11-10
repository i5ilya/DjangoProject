import os
from urllib.parse import urlparse
from collections import Counter
import requests
from django.core.files.base import ContentFile, File
from django.utils import timezone
from requests import Request, Session

from core import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django

django.setup()
from products.models import Product, Folder
from orders.models import Order

all_Folder = Folder.objects.all()
all_products = Product.objects.all()
tree = Folder.get_tree()

all_orders = Order.objects.all()

diction = {}

for items in all_products:
    diction[items.folder_id] = items.name


def get_name(id):
    return Folder.objects.get(id=id)


def get_id(name):
    return Folder.objects.get(name=name)


def create_folder_old(id, name, depth, numchild, parent_id):
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
        get_name(parent_id).add_child(id=id, name=name, depth=depth, numchild=numchild)  # в остальных случаях создаем папки в иерархии

def create_folder(id, name, parent_id):
    '''
    :param id: "ID" servio
    :param name: "Name" servio
    :param parentid: "ParentID" - root folder
    :param depth: "HierarchyLevel"  == 1 for MENU (identical for Django DB)
    :return: do writing folders in DB
    '''
    if parent_id == 0:  # в сервио parentid == 0 - это корневая папка
        pass  # должна быть создана в БД с кодом сервио и мы ее не обрабатываем
    else:
        Folder.objects.get(id=parent_id).add_child(id=id, name=name)  # в остальных случаях создаем папки в иерархии


def move_folder(id, parent_id):
    '''
    id - кого перемещаем
    parent_id - папка родитель куда перемещаем.
    '''
    Folder.objects.get(id=id).move(Folder.objects.get(parent_id), 'sorted-child')


def create_product(id, name, folder_id, price, image='images/default.jpg'):
    '''
    :param id: "ID" Servio
    :param name: "Name" Servio
    :param folder_id: "ParentID" Servio
    :param price: "Price" Servio
    :return: do writing new product in DB
    '''
    new_product = Product(id=id, folder=Folder.objects.get(id=folder_id), name=name, price=price, image_file=image)
    new_product.save()





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


def get_and_set_remote_image(some_url, product_id):
    '''
    Скачиваем и устанавливаем картинку как файл
    '''
    response = requests.get(some_url)
    file_name = urlparse(some_url).path.split('/')[-1]
    product = Product.objects.get(id=product_id)
    if response.status_code == 200:
        return product.image_file.save(file_name, ContentFile(response.content), save=True)


def set_image_file(path_file, product_id):
    product = Product.objects.get(id=product_id)
    product.image_file.name = path_file
    product.save()




if __name__ == '__main__':
    # create_folder(7777, 'cook', 4626)
    # create_product(268, 'test_beer-2', 7235, 126)

    # s = Session.objects.get(pk = '6q6rmhorut193osucpgnzecoouiku10x')
    # print(s.get_decoded())
    # for item in all_orders:
    #     total = item.get_total_cost()
    #     print(total)

    products_json = []

    for item in all_products:
        # print(item.id, item.name, item.folder.id, item.price, item.image_file)
        products_json.append({
            'id': item.id,
            'name': item.name,
            'folder.id': item.folder.id,
            'price': float(item.price),
            'product_image': item.image_file.url.replace('/media/', '')

        })

    products_json = {'products' : products_json}
    #print(products_json)



    #move_folder(7270, 1)
    instance = Folder.objects.get(id=7270)
    instance.delete()