# Generated by Django 3.1.1 on 2021-06-03 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_userdetails_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='week',
        ),
    ]
