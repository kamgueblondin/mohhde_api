import random
import string

from django.db import models
from django.contrib.auth.models import User


def generate_unique_code():
    length = 6
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Conversation.objects.filter(code=code).exists():
            return code

class ConversationState(models.TextChoices):
    ACTIVE = 'ACTIVE', 'Active'
    ARCHIVED = 'ARCHIVED', 'Archived'


class MessageState(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    READ = 'READ', 'Read'

class MessageStatus(models.TextChoices):
    NORMAL = 'NORMAL', 'Normal'
    MODIFIED = 'MODIFIED', 'Modified'
    DELETED = 'DELETED', 'Deleted'

class Conversation(models.Model):
    participants = models.ManyToManyField(User)
    code = models.CharField(max_length=10, unique=True, default=generate_unique_code)
    state=models.CharField(
		max_length=8,
		choices=ConversationState.choices,
		default=ConversationState.ACTIVE
	)


class MessageType(models.TextChoices):
    MSG = 'MSG', 'Generic Message'
    TXT = 'TXT', 'Text'
    JPEG = 'JPEG', 'JPEG Image'
    PNG = 'PNG', 'PNG Image'
    GIF = 'GIF', 'GIF Image'
    BMP = "BMP", "BMP Image"
    MP4 = "MP4", "MP4"
    AVI = "AVI", "AVI"
    MOV = "MOV", "MOV"
    MP3 = "MP3", "MP3"
    WAV = "WAV", "WAV"
    AAC = "AAC", "AAC"
    DOC = "DOC", "DOC"
    DOCX = "DOCX", "DOCX"
    PDF = "PDF", "PDF"
    XLS = "XLS", "XLS"
    XLSX = "XLSX", "XLSX"
    ZIP = "ZIP", "ZIP"
    RAR = "RAR", "RAR"
    ZZ = "7Z", "7Z"
    HTML = "HTML", "HTML"
    HTM = "HTM", "HTM"
    EXE = "EXE", "EXE"
    APK = "APK", "APK"
    MAP = "MAP", "MAP"
    HH = "H#H", "H#H"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    
	# Champ parent pour gérer la relation entre messages (facultatif)
	
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

	# Champ type pour définir le type de message
	
    type_of_message= models.CharField(max_length=4, choices=MessageType.choices, default=MessageType.MSG)

    
    state=models.CharField(max_length=7, choices=MessageState.choices, default=MessageState.PENDING)

    status=models.CharField(max_length=10, choices=MessageStatus.choices, default=MessageStatus.NORMAL)
                                      
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
	
    timestamp=models.DateTimeField(auto_now_add=True)