import os
from datetime import timedelta
#from products.models import Folder, Product
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from servio.models import Servio
from django.utils import timezone


class Connection():
    def __init__(self, s_id):
        self.servio = Servio.objects.get(id=s_id)
        self.url_main = self.servio.url_main
        self.cardcode = self.servio.cardcode
        self.termid = self.servio.termid
        self.token = self.servio.token
        self.updated = self.servio.updated
        self.body = {
            "CardCode" : self.cardcode,
            "TermID" : self.termid
            }
        self.url_auth = self.url_main + '/Authenticate'
        self.url_tarifitems = self.url_main + '/Get_TarifItems'
        self.headers = {"accesstoken": self.servio.token}

    def token_valid(self):
        if timezone.now() - timedelta(hours=23) < self.updated:
            return True
        else:
            return False

    def auth(self):
        if self.token_valid():
            pass
        else:
            try:
                response = requests.post(self.url_auth, json=self.body)
                if response.status_code == 200:
                    data_response = response.json()
                    self.servio.token = data_response['Token']
                    self.servio.save()
            except Exception as error:
                print(f"The error '{error}' occurred")

    def get_tarifitems(self):
        self.auth()
        try:
            response = requests.post(self.url_auth + self.url_tarifitems, headers=self.headers)
            if response.status_code == 200:
                data_response = response.json()
                return data_response['Items']
        except Exception as error:
            print(f"The error '{error}' occurred")

if __name__ == '__main__':

    s = Connection(1)
    # print(servio.updated)
    #print((timezone.now() - servio.updated)  < 12)
    for items in s.get_tarifitems():
        print(items['ID'])
        print(items['Name'])
        print(items['ParentID'])
        print('---------')
