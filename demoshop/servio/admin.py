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
        updated = 0
        for obj in queryset:
            sync = Syncing(obj.id)
            updated += 1
            if sync.auth():
                messages.error(request, sync.auth())
            else:
                sync.sync_folders()
                sync.sync_products()
                # self.message_user(request, ngettext(
                # '%d Sync was successfully completed.',
                # '%d Sync was successfully completed.',
                # updated,
                # ) % updated)
                messages.success(request, 'Sync was successfully completed')