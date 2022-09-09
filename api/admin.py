from django import forms
from django.contrib import admin
from api.models import serviceLogModel, serviceStatusTypeModel, settingsModel, userModel, vehicleModel, NotificationModel, vehicleTypeModel
from django.db import models
from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.utils.html import format_html

# Register your models here.

def completed(modeladmin, request, queryset):
    for object in queryset:
        object.statusType.name == 'Completed'
        object.save()
completed.short_description = 'Completed'

def servicing(modeladmin, request, queryset):
    for object in queryset:
        object.statusType.name == 'Servicing'
        object.save()
servicing.short_description = 'Servicing'

class addressAdmin(admin.ModelAdmin):
    list_display = ["province", 'city', 'address', 'deleteStatus']

    list_filter = ("province", 'city', 'deleteStatus')

    search_fields = ("address__contains", )

    def get_form(self, request, obj=None, **kwargs):
        form = super(addressAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].label_from_instance = lambda inst: "{} {}".format(
            inst.firstName, inst.lastName)
        return form


class userTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]

    # list_filter = ("name")

    search_fields = ("name__contains", )


class serviceStatusTypeAdmin(admin.ModelAdmin):
    list_display = ["id",
    "name"]

    # list_filter = ("name")

    search_fields = ("name__contains", )


class userAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image: 
            return format_html('<a href="{}" target="_blank"><img src="{}" width="80px"/></a>'.format(obj.id, obj.image.url))
        return obj.firstName
    image_tag.short_description = 'Image'

    
    list_display = [ 'id', 'image_tag', "firstName", 'lastName', 'email', 'phone',  'dateOfRegistration']

    list_filter = ('gender', 'phoneStatus', 'dateOfRegistration')

    search_fields = ("firstName__contains", )

    def get_form(self, request, obj=None, **kwargs):
        form = super(userAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields['address'].label_from_instance = lambda inst: "{}".format(
        #     inst.address)
        # form.base_fields['userType'].label_from_instance = lambda inst: "{}".format(
        #     inst.name)
        return form


class notificationAdmin(admin.ModelAdmin):
    list_display = ["message"]

    search_fields = ("phone__contains", )

    def get_form(self, request, obj=None, **kwargs):
        form = super(notificationAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields['user'].label_from_instance = lambda inst: "{} {}".format(
        #     inst.firstName, inst.lastName)
        return form


class vehicleAdmin(admin.ModelAdmin):
    list_display = [ "id", "blueBookOwnerName" ,"licensePlateNumber", "brand", 'model', "color"]
    list_filter = ("brand", 'model')

    search_fields = ("brand__contains", "blueBookOwnerName")

    def get_form(self, request, obj=None, **kwargs):
        form = super(vehicleAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].label_from_instance = lambda inst: "{} {}".format(
            inst.firstName, inst.lastName)
        form.base_fields['vehicleType'].label_from_instance = lambda inst: "{}".format(
            inst.name)
        return form


class serviceLogAdmin(admin.ModelAdmin):
    def username_tag(self, obj):
        return obj.user.firstName
    username_tag.short_description = 'Username'

    status = models.ForeignKey(
        "serviceStatusTypeModel",
        related_name="service_type",
        on_delete=models.CASCADE,
        default=1,
        null=True,
        blank=True,
    )

    def status(self, request):
        if request.statusType.name == "Completed":
             return format_html(
            '<span style="background-color: green; color: white; padding: 8px; font-weight: bold;">{}</span>', 'Completed'
             )
        elif request.statusType.name == "Servicing":
             return format_html(
            '<span style="background-color: blue; color: white; padding: 8px; font-weight: bold;">{}</span>', request.statusType.name
            )
        else:
             return format_html(
            '<span style="background-color: red; color: white; padding: 8px; font-weight: bold;">{}</span>', request.statusType.name
            )
    status.allow_tags = True

    list_display = ['id', 'user', 'username_tag', "dateOfMaintanance", "vehicle",
                    "deleteStatus", "status"]

    actions = [completed, servicing]
    
    # class Media: 
    #     js = ("admin/js/new_ajax.js",)

    list_filter = ("deleteStatus", 'statusType', 'dateOfMaintanance')

    # search_fields = ("brand__contains", ) 

    # readonly_fields=('user', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(serviceLogAdmin, self).get_form(request, obj, **kwargs)
        # form.base_fields['user'].label_from_instance = lambda inst: "{}".format(
        #     inst.phone)
        form.base_fields['vehicle'].label_from_instance = lambda inst: "{}".format(
            inst.licensePlateNumber)
        form.base_fields['statusType'].label_from_instance = lambda inst: "{}".format(
            inst.name)
        # form.base_fields['address'].label_from_instance = lambda inst: "{}".format(
        # inst.address)
        return form


class settingsAdmin(admin.ModelAdmin):
    list_display = ["id"]


class vehicleTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


class sessionAdmin(admin.ModelAdmin):
    list_display = ["id"]


class otpAdmin(admin.ModelAdmin):
    list_display = ["otp"]



admin.site.register(vehicleTypeModel, vehicleTypeAdmin)
admin.site.register(settingsModel, settingsAdmin)
# admin.site.register(otpModel, otpAdmin)
# admin.site.register(sessionModel, sessionAdmin)
admin.site.register(vehicleModel, vehicleAdmin)
# admin.site.register(notificationLogModel, notificationAdmin)
admin.site.register(userModel, userAdmin)
admin.site.register(serviceStatusTypeModel, serviceStatusTypeAdmin)
# admin.site.register(userTypeModel, userTypeAdmin)
# admin.site.register(addressModel, addressAdmin)
admin.site.register(serviceLogModel, serviceLogAdmin)
admin.site.register(NotificationModel, notificationAdmin)
# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin.site.unregister(Site)
