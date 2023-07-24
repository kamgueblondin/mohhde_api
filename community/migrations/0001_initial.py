# Generated by Django 4.0 on 2023-07-23 19:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Communaute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('nombre_utilisateurs', models.IntegerField()),
                ('objectif', models.TextField()),
                ('contacts', models.TextField()),
                ('est_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Administrateur'), ('moderateur', 'Modérateur'), ('invite', 'Invité')], max_length=20)),
                ('communaute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='community.communaute')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]