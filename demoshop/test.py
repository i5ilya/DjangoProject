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


def create_folder(id, name, numchild, parent_id, depth):
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
        get_name(parent_id).add_child(id=id, name=name, numchild=numchild, depth=depth)  # в остальных случаях создаем папки в иерархии


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
    # create_folder(7777, 'cook', 1, 2)
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

    url_auth = "https://17.servio.support/29099/POSExternal/Authenticate"
    url_tarifitems = 'https://17.servio.support/29099/POSExternal/Get_TarifItems'
    data = {
            "CardCode" : "777",
            "TermID" : "ANDROID"
            }
    response = requests.post(url_auth, json=data)
    #r = requests.post(url=URL, params=PARAMS)
    print("Status Code", response.status_code)
    data_response = response.json()
    token = data_response['Token']
    print(token)
    response_tarifitems = requests.post(url_tarifitems, headers={"accesstoken": token})
    data_response_tarifitems = response_tarifitems.json()

    print(data_response_tarifitems['Items'])
    folder_parent_ids = []
    for item in data_response_tarifitems['Items']:
        if item['ParentID'] != 0:
            folder_parent_ids.append(item['ParentID'])

    count = Counter(folder_parent_ids) # количество повторений 'ParentID' во всем списке

    for item in data_response_tarifitems['Items']:
        print(item['ID'])
        print(item['Name'])
        print(count[item['ID']])
        print(item['ParentID'])
        print(item['HierarchyLevel'])