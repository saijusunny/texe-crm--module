# Generated by Django 4.0.2 on 2023-12-21 08:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regno', models.CharField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('email', models.CharField(blank=True, max_length=250, null=True)),
                ('number', models.CharField(blank=True, max_length=250, null=True)),
                ('password', models.CharField(blank=True, max_length=250, null=True)),
                ('profile', models.ImageField(blank=True, default='static\\images\\static_image\\icon.svg', null=True, upload_to='images/propic')),
                ('joindate', models.DateField(default=datetime.date(2023, 12, 21), null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, default='active', max_length=255, null=True)),
                ('addres', models.TextField(blank=True, null=True)),
                ('role', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateField(null=True)),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('otp', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]