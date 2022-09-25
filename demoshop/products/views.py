from django.shortcuts import render, get_object_or_404
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


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product_detail.html', {'product': product})

def folder_list(request, folder_slug):
    folder = get_object_or_404(Folder, slug=folder_slug)
    products = Product.objects.filter(folder=folder)
    return render(request, 'folder.html', {'folder': folder, 'products': products})



class FolderView(ModelViewSet):  # this for json api
    queryset = Folder.objects.all()
    serializer_class = FolderSerializer
