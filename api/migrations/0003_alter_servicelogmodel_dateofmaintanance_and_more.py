# Generated by Django 4.0.4 on 2022-05-23 07:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_servicelogmodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelogmodel',
            name='dateOfMaintanance',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='dateOfRegistration',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vehiclemodel',
            name='blueBookExpiryDate',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='vehiclemodel',
            name='blueBookRenewalDate',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
    ]
