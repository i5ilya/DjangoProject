from rest_framework.serializers import ModelSerializer
from products.models import Folder, Product


class FolderSerializer(ModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
        #fields = ["name", "id"]
