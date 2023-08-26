from django.contrib import admin

# Register your models here.
from .models import Stock,Element

admin.site.register(Stock)
admin.site.register(Element)
