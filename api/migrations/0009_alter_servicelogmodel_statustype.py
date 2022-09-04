# Generated by Django 4.0.4 on 2022-05-31 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_addressmodel_droplocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelogmodel',
            name='statusType',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_type', to='api.servicestatustypemodel'),
        ),
    ]
