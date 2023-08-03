# Generated by Django 4.0 on 2023-07-26 06:58

import chat.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=chat.models.generate_unique_code, max_length=10, unique=True)),
                ('state', models.CharField(choices=[('ACTIVE', 'Active'), ('ARCHIVED', 'Archived')], default='ACTIVE', max_length=8)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_message', models.CharField(choices=[('MSG', 'Generic Message'), ('TXT', 'Text'), ('JPEG', 'JPEG Image'), ('PNG', 'PNG Image'), ('GIF', 'GIF Image'), ('BMP', 'BMP Image'), ('MP4', 'MP4'), ('AVI', 'AVI'), ('MOV', 'MOV'), ('MP3', 'MP3'), ('WAV', 'WAV'), ('AAC', 'AAC'), ('DOC', 'DOC'), ('DOCX', 'DOCX'), ('PDF', 'PDF'), ('XLS', 'XLS'), ('XLSX', 'XLSX'), ('ZIP', 'ZIP'), ('RAR', 'RAR'), ('7Z', '7Z'), ('HTML', 'HTML'), ('HTM', 'HTM'), ('EXE', 'EXE'), ('APK', 'APK'), ('MAP', 'MAP'), ('H#H', 'H#H')], default='MSG', max_length=4)),
                ('state', models.CharField(choices=[('PENDING', 'Pending'), ('READ', 'Read')], default='PENDING', max_length=7)),
                ('status', models.CharField(choices=[('NORMAL', 'Normal'), ('MODIFIED', 'Modified'), ('DELETED', 'Deleted')], default='NORMAL', max_length=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.conversation')),
                ('parent_message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chat.message')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
