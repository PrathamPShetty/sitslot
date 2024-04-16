# Generated by Django 4.1.5 on 2024-04-14 19:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('images', models.ImageField(upload_to='place_photo')),
                ('img1', models.ImageField(blank=True, default='', null=True, upload_to='place_photo')),
                ('img2', models.ImageField(blank=True, default='', null=True, upload_to='place_photo')),
                ('img3', models.ImageField(blank=True, default='', null=True, upload_to='place_photo')),
                ('img4', models.ImageField(blank=True, default='', null=True, upload_to='place_photo')),
                ('img5', models.ImageField(blank=True, default='', null=True, upload_to='place_photo')),
                ('introduction', models.CharField(blank=True, default='', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('event', models.CharField(max_length=100)),
                ('date', models.DateField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('start_time', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('end_time', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0))),
                ('image', models.ImageField(upload_to='image')),
                ('discription', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('location', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('myuser', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.places')),
            ],
        ),
        migrations.CreateModel(
            name='display',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.event')),
            ],
        ),
    ]
