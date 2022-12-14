from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify
from treebeard.mp_tree import MP_Node


# Create your models here.


class Folder(MP_Node):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, null=True)
    node_order_by = ['name']

    def save(self, *args, **kwargs):
        super(Folder, self).save(*args, **kwargs)
        self.slug = slugify(f'folder-{self.id}')
        super(Folder, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('folder_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    # tarif_item_id = models.IntegerField(unique=True, null=True, blank=True)  # TarifItemID Servio
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, null=True)
    image_file = models.ImageField(upload_to='images/', blank=True, default='images/default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)  # сохраняем, чтобы получить id
        self.slug = slugify(f'product-{self.id}')
        super(Product, self).save(*args, **kwargs)  # сохраняем после сделанных нами действий.

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    def image_url(self):
        if self.image_file and hasattr(self.image_file, 'url'):
            return self.image_file.url

    def __str__(self):
        return self.name


# @receiver(post_save, sender=Product)
# def post_save_product(sender, instance, created, **kwargs):
#     if created:
#         instance.slug = slugify(f'product-{instance.id}')
#         instance.save(update_fields=['slug'])


# @receiver(post_save, sender=Folder)
# def post_save_folder(sender, instance, created, **kwargs):
#     if created:
#         instance.slug = slugify(f'folder-{instance.id}')
#         instance.save(update_fields=['slug'])
