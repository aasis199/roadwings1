from vehicle.settings import STATIC_URL
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from .views import *

urlpatterns = [
    path("user/register/", views.userRegister, name="userregister"),
    path("user/login/", views.userLogin, name="userLogin"),
    path("user/logout/", views.userLogout, name="userLogout"),
    path("user/forgot_password/", views.userForgotPass, name="userForgotPass"),
    #
    path("user/profile/", views.userProfile, name="userProfile"),
    path("user/editprofile/", views.userEditProfile, name="userEditProfile"),
    #

    path("user/otp/", views.userSendOtp, name="usersendotp"),
     path("user/forgototp/", views.userForgotSendOtp, name="usersendotp"),
    path("user/checkotp/", views.userCheckOtp, name="usercheckotp"),
    #
    path("user/vehicle/", views.userVehicle, name="uservehicle"),
    path("user/createvehicle/", views.userCreateVehicle, name="usercreatevehicle"),
    path("user/editvehicle/", views.userEditVehicle, name="usereditvehicle"),
    path("user/deletevehicle/", views.userDeleteVehicle, name="userdeletevehicle"),
    #
    path("user/address/", views.userAddress, name="useraddress"),
    path("user/createaddress/", views.userCreateAddress, name="usercreateaddress"),
    path("user/editaddress/", views.userEditAddress, name="usereditaddress"),
    path("user/deleteaddress/", views.userDeleteAddress, name="userdeleteaddress"),
    #
    path("user/service/", views.userService, name="useraService"),
    path("user/createservice/", views.userCreateService, name="usercreateService"),
    path("user/editservice/", views.userEditService, name="usereditService"),
    path("user/deleteservice/", views.userDeleteService, name="userdeleteService"),
    # path('users/', UserList.as_view()),
    #
]

admin.site.site_header = 'Roadwings Administration'
