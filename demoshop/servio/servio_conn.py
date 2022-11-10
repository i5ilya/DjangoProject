# need fo run this file
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()

# need and working with django native
from servio.models import Servio
from django.utils import timezone
import requests
from django.utils.datetime_safe import datetime
from products.models import Folder, Product
from typing import *
from urllib.parse import urlparse
from django.core.files.base import ContentFile


class Connection():
    def __init__(self, s_id):
        self.servio = Servio.objects.get(id=s_id)
        self.url_main = self.servio.url_main
        self.cardcode = self.servio.cardcode
        self.termid = self.servio.termid
        self.token = self.servio.token
        self.token_valid = self.servio.token_valid
        self.body = {
            "CardCode": self.cardcode,
            "TermID": self.termid
        }
        self.url_auth = self.url_main + '/Authenticate'
        self.url_tarifitems = self.url_main + '/Get_TarifItems'
        self.url_tarifitem = self.url_main + '/Get_TarifItem'
        self.headers = {"accesstoken": self.token}

    def auth(self):
        if self.token_valid < timezone.now():
            try:
                response = requests.post(self.url_auth, json=self.body)
                if response.status_code == 200:
                    data_response = response.json()
                    if data_response.get('Success') is not None:  # Если в словаре есть ключ
                        if not data_response['Success']:  # Если этот ключ не True
                            print(data_response['Error'])
                    else:
                        self.servio.token = data_response['Token']
                        self.token = self.servio.token
                        self.headers = {"accesstoken": self.token}
                        time_token_convert = datetime.strptime(data_response['Valid'], '%Y.%m.%d %H:%M:%S')
                        self.servio.token_valid = timezone.make_aware(time_token_convert,
                                                                      timezone.get_current_timezone())
                        self.token_valid = self.servio.token_valid
                        self.servio.save()
            except Exception as error:
                print(f"The error '{error}' occurred")

    def get_tarifitems(self):
        self.auth()
        try:
            response = requests.post(self.url_auth + self.url_tarifitems, headers=self.headers)
            data_response = response.json()
            if response.status_code == 401:
                if data_response.get('Success') is not None:  # Если в словаре есть ключ
                    if not data_response['Success']:  # Если этот ключ не True
                        print(data_response['Error'])
            if response.status_code == 200:
                return data_response['Items']
        except Exception as error:
            print(f"The error {error} occurred")


    def get_tarifitem(self):
        self.auth()
        try:
            response = requests.post(self.url_auth + self.url_tarifitem, headers=self.headers)
            data_response = response.json()
            if response.status_code == 401:
                if data_response.get('Success') is not None:  # Если в словаре есть ключ
                    if not data_response['Success']:  # Если этот ключ не True
                        print(data_response['Error'])
            if response.status_code == 200:
                return data_response['Item']
        except Exception as error:
            print(f"The error {error} occurred")

class Syncing(Connection):
    def __init__(self, s_id):
        super().__init__(s_id)
        # folder part
        self.folders = Folder.objects.all()
        if self.get_tarifitems():
            self.servio_folders = self.get_tarifitems()
            self.root_folder_id_in_servio = [item["ID"] for item in self.servio_folders if item['ParentID'] == 0]
            self.ids_servio_folders = {item["ID"] for item in self.servio_folders}
        self.ids_site_folders = {item.id for item in self.folders}


        # Product part
        self.products = Product.objects.all()
        if self.get_tarifitem():
            self.servio_products = self.get_tarifitem()
            self.ids_servio_products = {item["ID"] for item in self.servio_products}
            self.parent_ids_servio_products = {item['ParentID'] for item in self.servio_products}
        self.ids_site_products = {item.id for item in self.products}
    # start folder part ------------------------------------------------------------------------------------------
    def exist_root_folder(self):
        for element in self.ids_site_folders:
            if element in self.root_folder_id_in_servio and Folder.objects.get(id=element).depth == 1:
                return True
        return False

    def fix_tree(self):
        Folder.objects.get(id=self.root_folder_id_in_servio[0]).fix_tree()
    def find_deleted_servio_folders_ids(self):
        print(self.ids_servio_folders)
        print(self.ids_site_folders)
        deleted_folders = self.ids_site_folders - self.ids_servio_folders

        if len(deleted_folders) != 0:
            print(deleted_folders)
            return deleted_folders
        return False

    def create_folder(self, id, name, parent_id):
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

    def delete_folders(self, folders_ids:set):
        '''
        forders_ids - set of ids.
        '''
        if folders_ids:
            for item in folders_ids:
                instance = Folder.objects.get(id=item)
                instance.delete()

    def sync_folders(self):
        find_deleted_servio_folders_ids = self.find_deleted_servio_folders_ids()
        if find_deleted_servio_folders_ids:
            self.delete_folders(find_deleted_servio_folders_ids)
            self.fix_tree()

        if self.exist_root_folder():
            for item in self.servio_folders:
                if item['ParentID'] in self.ids_site_folders:
                    self.create_folder(item['ID'], item['Name'], item['ParentID'])
                    self.fix_tree()
        self.folders = Folder.objects.all()
        self.ids_site_folders = {item.id for item in self.folders}

    # end folder part ------------------------------------------------------------------------------------------
    # start product part ------------------------------------------------------------------------------------------
    def create_product(self, id, name, folder_id, price):
        '''
        :param id: "ID" Servio
        :param name: "Name" Servio
        :param folder_id: "ParentID" Servio
        :param price: "Price" Servio
        :return: do writing new product in DB
        '''
        new_product = Product(id=id, folder=Folder.objects.get(id=folder_id), name=name, price=price)
        new_product.save()

    def get_and_set_remote_image(self, some_url, product_id):
        '''
        Скачиваем и устанавливаем картинку как файл
        '''
        response = requests.get(some_url)
        file_name = urlparse(some_url).path.split('/')[-1]
        product = Product.objects.get(id=product_id)
        if response.status_code == 200:
            return product.image_file.save(file_name, ContentFile(response.content), save=True)

    def set_image_file(self, path_file, product_id):
        product = Product.objects.get(id=product_id)
        product.image_file.name = path_file
        product.save()


    def sync_products(self):
        for item in self.servio_products:
            if item['ParentID'] in self.ids_site_folders:
                self.create_product(item['ID'], item['Name'], item['ParentID'], item['Price'])
                if item['PhotoUrl']:
                    self.get_and_set_remote_image(item['PhotoUrl'], item['ID'])


if __name__ == '__main__':
    #s = Connection(1)

    # print(s.updated)
    print(f'Сейчас {timezone.localtime(timezone.now())}')  # конвертация в localtime
    # print(timezone.now())
    # print((timezone.now() - servio.updated)  < 12)
    # print(f'Токен валидный до  {timezone.localtime(s.token_valid)}')
    # for items in s.get_tarifitems():
    #     print(items['ID'])
    #     print(items['Name'])
    #     print(items['ParentID'])
    #     print('---------')

    # for item in s.get_tarifitem():
    #     print(item['ID'])
    #     print(item['ParentID'])
    #     print(item['Name'])
    #     print(item['Price'])
    #     print(item['PhotoUrl'])

    sync = Syncing(1)

    #print(f'Токен валидный до  {timezone.localtime(sync.token_valid)}')
    #sync.sync_folders()
    # sync.deleted_servio_folders()
    #sync.delete_folders({7234})
    #sync.find_deleted_servio_folders()
    #sync.create_folder(1, 'test', 4626)
    #print(Folder.objects.get(id=4626).find_problems())
    #Folder.objects.get(id=4626).fix_tree()
    #new_node = Folder(name='root2')
    #Folder.objects.get(id=1).add_sibling('sorted-sibling', instance=new_node)
    sync.sync_folders()
    sync.sync_products()