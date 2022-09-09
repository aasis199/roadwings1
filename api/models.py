from argparse import FileType
from email.mime import image
from email.policy import default
from operator import truediv
from pyexpat import model
import requests
from django import dispatch
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
from django.utils import timezone
from datetime import datetime
from smart_selects.db_fields import ChainedForeignKey


GENDER = [
    ('male', 'male'),
    ('female', 'female'),
    ('others', 'others')
]


class addressModel(models.Model):
    name = models.CharField(max_length=255, default='')

    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255, default='')
    deleteStatus = models.BooleanField(default=False)
    user = models.ForeignKey(
        "userModel",
        related_name="address_user",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return self.name


class userTypeModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'User Type'
        verbose_name_plural = 'User Type'

    def __str__(self):
        return self.name


class serviceStatusTypeModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Service Status Type'
        verbose_name_plural = 'Service Status Type'

    def __str__(self):
        return self.name


class settingsModel(models.Model):
    sms_token = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Settings'
        verbose_name_plural = 'Settings'

    def __str__(self):
        return self.sms_token


class vehicleTypeModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Vehicle Type'
        verbose_name_plural = 'Vehicle Type'

    def __str__(self):
        return self.name

class notificationLogModel(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    file = models.FileField(
        upload_to="notificationfiles/",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        "userModel",
        related_name="notif_user",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


class userModel(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255)
    passw = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER,default='', blank=True, null=False, max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to="userimages/")
    phoneStatus = models.BooleanField(default=False)
    dateOfRegistration = models.DateField(null=True,blank=True,)
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    def __str__(self):
        return self.phone


class vehicleModel(models.Model):
    user = models.ForeignKey(userModel, related_name="vehicle_user",on_delete=models.CASCADE, default='')
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    licensePlateNumber = models.CharField(max_length=255)
    blueBookPhoto = models.ImageField( null=True, blank=True, upload_to="bluebook/")
    blueBookRenewalDate = models.DateField(null=True, blank=True,)
    blueBookExpiryDate = models.DateField(null=True,blank=True,)
    blueBookOwnerName = models.CharField(max_length=255)
    vehicleType = models.ForeignKey(
        "vehicleTypeModel",
        related_name="user_vehicleType",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Vehicle'
        verbose_name_plural = 'Vehicles'

    def get_user(self):
        return self.user

    def __str__(self):
        return self.licensePlateNumber

class serviceLogModel(models.Model):
    user = models.ForeignKey(userModel, related_name="user_vehicle",on_delete=models.CASCADE, default='')
    dropLocation = models.CharField(max_length=255, default='')
    pickUpLocation = models.CharField(max_length=255, default='')
    deleteStatus = models.BooleanField(default=False)
    statusType = models.ForeignKey("serviceStatusTypeModel", related_name="service_type", on_delete=models.CASCADE,default=1, null=True,blank=True,)
    invoice = models.FileField(upload_to="invoices/",null=True,blank=True,)
    dateOfMaintanance = models.DateTimeField(null=True,blank=True,)
    vehicle = ChainedForeignKey(
        vehicleModel,
        on_delete=models.CASCADE,
        chained_field="user",
        chained_model_field="user",
        show_all=False,
        auto_choose= True,
    )

    class Meta:
        verbose_name = 'Service Record'
        verbose_name_plural = 'Service Records'

    def __str__(self):
        return self.user.firstName
#
#


class sessionModel(models.Model):
    token = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    tim = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.token


class otpModel(models.Model):
    otp = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    tim = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.otp


class NotificationModel(models.Model):

    # name = models.CharField(max_length=255, default="")
    phone = models.CharField(max_length=250)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'SMS Notification'
        verbose_name_plural = 'SMS Notifications'

    def __str__(self):
        return self.phone


@receiver(post_save, sender=NotificationModel, dispatch_uid="send_message")
def update_stock(sender, instance, **kwargs):

    phone = instance.phone
    message = instance.message
    auth_token = settingsModel.objects.all()[0].sms_token
    data = {'auth_token': auth_token, 'to': phone, 'text': message}
    url = 'https://sms.aakashsms.com/sms/v3/send/'
    res = requests.post(url, data=data)
    res = res.json()
    print(res)

    if res['error']:
        return res['message']
    else:
        # instance.save()
        return 'success'
