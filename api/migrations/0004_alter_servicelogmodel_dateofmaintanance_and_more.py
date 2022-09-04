# Generated by Django 4.0.4 on 2022-05-23 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_servicelogmodel_dateofmaintanance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelogmodel',
            name='dateOfMaintanance',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='dateOfRegistration',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclemodel',
            name='blueBookExpiryDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclemodel',
            name='blueBookRenewalDate',
            field=models.DateField(blank=True, null=True),
        ),
    ]