from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Servio
from .servio_conn import Connection, Syncing


@admin.register(Servio)
class ServioAdmin(admin.ModelAdmin):
    list_display = ['url_main', 'updated']
    exclude = ['token_valid']
    actions = ['servio_sync']

    @admin.action(description='Sync menu Servio')
    def servio_sync(self, request, queryset):
        #updated = 0
        for obj in queryset:
            con = Connection(obj.id)
            #updated += 1
            auth_answer = con.auth()
            if auth_answer:
                messages.error(request, auth_answer)
            tarifitems_answer = con.get_tarifitems()
            if type(tarifitems_answer) != list:
                messages.error(request, tarifitems_answer)
            else:
                sync = Syncing(obj.id)
                sync.sync_folders()
                sync.sync_products()
                # self.message_user(request, ngettext(
                # '%d Sync was successfully completed.',
                # '%d Sync was successfully completed.',
                # updated,
                # ) % updated)
                messages.success(request, 'Sync was successfully completed')