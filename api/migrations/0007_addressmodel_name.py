# Generated by Django 4.0.4 on 2022-05-29 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_servicelogmodel_statustype'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressmodel',
            name='name',
            field=models.CharField(default='name', max_length=255),
            preserve_default=False,
        ),
    ]
