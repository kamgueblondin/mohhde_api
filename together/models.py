from django.db import models
from django.contrib.auth.models import User

from chat.models import Conversation

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_friend')
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('blocked', 'Blocked')))
    category = models.CharField(max_length=20, choices=(('family', 'Family'), ('love', 'Love'), ('friend', 'Friend'), ('classmate', 'Classmate')))
    conversation = models.ForeignKey(Conversation, on_delete=models.SET_NULL,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)