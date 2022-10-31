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
from products.models import Folder


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
                print('test')
                return data_response['Items']
        except Exception as error:
            print(f"The error '{error}' occurred")


class Syncing(Connection):
    def __init__(self, s_id):
        super().__init__(s_id)
        self.folders = Folder.objects.all()
        self.servio_folders = self.get_tarifitems()
    def exist_root_folder(self):
        root_folder_id_in_servio = [item["ID"] for item in self.servio_folders if item['ParentID'] == 0]
        all_folders_ids_database = [item.id for item in self.folders]
        for element in all_folders_ids_database :
            print(Folder.objects.get(id=element).depth)
            if element in root_folder_id_in_servio and Folder.objects.get(id=element).depth == 1:
                return True
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



if __name__ == '__main__':
    # s = Connection(1)
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
    sync = Syncing(1)
    print(f'Токен валидный до  {timezone.localtime(sync.token_valid)}')
    print(sync.exist_root_folder())
