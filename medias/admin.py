from django.contrib import admin

# Register your models here.
from .models import Chain,Media,Subscription,Filter,ChannelList

admin.site.register(Chain)
admin.site.register(Media)
admin.site.register(Subscription)
admin.site.register(Filter)
admin.site.register(ChannelList)