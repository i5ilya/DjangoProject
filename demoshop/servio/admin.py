from django.contrib import admin
from django.utils.translation import ngettext

from .models import Servio
#from .servio_conn import Connection


@admin.register(Servio)
class ServioAdmin(admin.ModelAdmin):
    list_display = ['url_main', 'updated']
    exclude = ['token_valid']
    actions = ['servio_sync']

    # @admin.action(description='Sync menu Servio')
    # def servio_sync(self, request, queryset):
    #     updated = 0
    #     for obj in queryset:
    #         s = Connection(obj.id)
    #         updated += 1
    #         s.get_tarifitems()
    #     self.message_user(request, ngettext(
    #         '%d Sync was successfully completed.',
    #         '%d Sync was successfully completed.',
    #         updated,
    #     ) % updated)
