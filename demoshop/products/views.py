from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from products.models import Folder
from products.models import Product
from products.serializers import FolderSerializer


def folders(request):
    return {
        'folders': Folder.get_annotated_list()
    }


def all_products(request):
    products = Product.objects.all()
    # context = {'tree': tree, 'products': products, 'tree1': tree1}
    return render(request, 'home.html', {'products': products})


class FolderView(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
