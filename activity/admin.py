from django.contrib import admin

from .models import Activite, Communaute, Membre


admin.site.register(Activite)
admin.site.register(Communaute)
admin.site.register(Membre)
