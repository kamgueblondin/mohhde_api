from django.urls import path
from chat.views import chat, room, ConversationMessagesAPIView,mohhassistantAPIView

urlpatterns = [
    path('chat/', chat, name='chat_index'),
    path('chat/<str:room_name>/', room, name="chat_room"),
    path('api/conversations/messages/', ConversationMessagesAPIView.as_view(), name='conversation-messages'),
    path('api/mohhassistant/messages/', mohhassistantAPIView.as_view(), name='mohhassistant-messages'),
]