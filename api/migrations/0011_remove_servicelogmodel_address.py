# Generated by Django 4.0.4 on 2022-06-06 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_remove_addressmodel_droplocation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicelogmodel',
            name='address',
        ),
    ]
