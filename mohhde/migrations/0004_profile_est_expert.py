# Generated by Django 4.0 on 2023-10-08 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mohhde', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='est_expert',
            field=models.BooleanField(default=False),
        ),
    ]
