from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from products.models import Folder
from products.models import Product
from products.serializers import FolderSerializer


def products_page(request):
    tree = Folder.dump_bulk()
    products = Product.objects.all()
    context = {'tree': tree, 'products': products}
    # return render(request, 'index.html', {'tree': tree})
    return render(request, 'index.html', context=context)


class FolderView(ModelViewSet):
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
