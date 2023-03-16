from django.contrib import admin
from .models import Mygifts
from .models import Messages


class GiftAdmin(admin.ModelAdmin):
    list_display = ("title", "body")


admin.site.register(Mygifts, GiftAdmin)
admin.site.register(Messages)
