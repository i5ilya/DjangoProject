from django.db import models


# Create your models here.


class Servio(models.Model):
    url_main = models.CharField(max_length=100, db_index=True)
    cardcode = models.CharField(max_length=100, db_index=True)
    termid = models.CharField(max_length=100, db_index=True)
    token = models.CharField(max_length=100, db_index=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Servio'
        verbose_name_plural = 'Servio'

    def __str__(self):
        return f'servio {self.id}'
