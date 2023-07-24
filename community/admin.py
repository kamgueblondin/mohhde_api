from django.contrib import admin

# Register your models here.
from .models import Communaute,Participant

admin.site.register(Communaute)
admin.site.register(Participant)