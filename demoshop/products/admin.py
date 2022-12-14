from django.contrib import admin
# Register your models here.
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from .models import Folder, Product


@admin.register(Folder)
class FolderAdmin(TreeAdmin):
    form = movenodeform_factory(Folder)


# admin.site.register(Folder, FolderAdmin)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['folder', 'name', 'price']
    list_filter = ['folder']
    list_editable = ['name', 'price']

# admin.site.register(Product, ProductAdmin)
