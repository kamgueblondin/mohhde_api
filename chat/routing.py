from django.urls import re_path,path
from chat.consumers import RoomConsumer,ChatConsumer

ws_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', RoomConsumer.as_asgi()),
    #path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
]
