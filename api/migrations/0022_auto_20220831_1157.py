# Generated by Django 2.2 on 2022-08-31 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20220831_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('others', 'others')], default='', max_length=50),
        ),
    ]
