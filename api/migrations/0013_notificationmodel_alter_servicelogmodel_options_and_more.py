# Generated by Django 4.0.4 on 2022-06-09 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_alter_servicelogmodel_dateofmaintanance'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('number', models.IntegerField(default=0)),
                ('message', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='servicelogmodel',
            options={'verbose_name': 'Service Record', 'verbose_name_plural': 'Service Records'},
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='address',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='deviceId',
        ),
        migrations.RemoveField(
            model_name='usermodel',
            name='userType',
        ),
    ]
