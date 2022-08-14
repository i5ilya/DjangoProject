from django.db import models
from treebeard.mp_tree import MP_Node
# Create your models here.



class Folder(MP_Node):
    name = models.CharField(max_length=30)
    node_order_by = ['name']

    # def __str__(self):
    #     return 'Folder: {}'.format(self.name)
    def __str__(self):
        return self.name


class Product(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    #tarif_item_id = models.IntegerField(unique=True, null=True, blank=True)  # TarifItemID Servio
    name = models.CharField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
