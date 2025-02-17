# Generated by Django 4.0 on 2022-12-07 18:58

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('home', '0002_alter_model_data_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, default=None, null=True, storage=django.core.files.storage.FileSystemStorage(location='assets/images'), upload_to='')),
                ('personal_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('bio', models.CharField(blank=True, max_length=1000, null=True)),
                ('date_joined', models.DateTimeField(blank=True, default=None, null=True)),
                ('reset_token', models.CharField(blank=True, max_length=1000, null=True)),
                ('reset_link', models.CharField(blank=True, max_length=1000, null=True)),
                ('token_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user')),
            ],
            options={
                'verbose_name': 'Profile',
                'ordering': ('user',),
            },
        ),
    ]
