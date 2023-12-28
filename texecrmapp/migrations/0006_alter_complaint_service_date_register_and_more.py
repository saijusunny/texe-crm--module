# Generated by Django 4.0.2 on 2023-12-28 08:42

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('texecrmapp', '0005_users_complaint_users_orders_users_preformance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint_service',
            name='date_register',
            field=models.DateField(default=datetime.date(2023, 12, 28)),
        ),
        migrations.AlterField(
            model_name='users',
            name='joindate',
            field=models.DateField(default=datetime.date(2023, 12, 28), null=True),
        ),
        migrations.CreateModel(
            name='events',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='texecrmapp.users')),
            ],
        ),
    ]