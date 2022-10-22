import os
from typing import Any
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from django.contrib.sessions.models import Session
from django.conf import settings
django.setup()
from django.core.management import call_command
from products.models import Product, Folder
from cart.cart import Cart
from orders.models import Order, OrderItem


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


# create_product(7231, 'Вино Кагор 150', 7234, 100)

tree_raw = Folder.dump_bulk()
annotated_list = Folder.get_annotated_list()

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



def get_remote_image(some_url):
    response = requests.get(some_url)
    file_name = urlparse(some_url).path.split('/')[-1]
    if response.status_code == 200:
        return file_name, response.content





if __name__ == '__main__':
    #create_folder(7777, 'cook', 1, 2)
    #create_product(268, 'test_beer-2', 7235, 126)


    # s = Session.objects.get(pk = '6q6rmhorut193osucpgnzecoouiku10x')
    # print(s.get_decoded())
    # for item in all_orders:
    #     total = item.get_total_cost()
    #     print(total)

    products_json = []

    for item in all_products:
        #print(item.id, item.name, item.folder.id, item.price, item.image_file)
        products_json.append({
            'product.id' : item.id,
            'product.name' : item.name,
            'product.folder.id' : item.folder.id,
            'product.price' : item.price,
            'product_image' : item.image_file.url

        })
    print(products_json)
    beer = Product.objects.get(name='test_beer-22')
    beer.image_file = 'images/photo-1608270586620-248524c67de9.jpg'

    url = 'https://i.imgur.com/inn42BF.jpeg'
    response = requests.get('https://i.imgur.com/9ByhOFK.jpeg')
    file_name = urlparse(url).path.split('/')[-1]
    print(file_name)
    beer.image_file.save(file_name, ContentFile(response.content), save=True)
    print(beer.image_file.url)