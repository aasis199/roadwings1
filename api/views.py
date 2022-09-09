import json
import django.db.models.fields
from django.forms.models import model_to_dict
from django.db.models.query_utils import Q
import datetime
from django.forms.models import model_to_dict
from django.http.response import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import os
from django.core.paginator import Paginator
from django.core.mail import BadHeaderError, send_mail
from smtplib import SMTPRecipientsRefused
from random import randint
import requests
from django.contrib import messages

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# from .env import *

from .models import addressModel, otpModel, serviceLogModel, sessionModel, settingsModel, userModel, vehicleModel
from .serializers import addressSerializer, serviceLogSerializer, userSerializer, vehicleSerializer
##########################################################################################################
##########################################################################################################

# def get_user(request):
#     vehicle = request.POST.get('project')
#     user = {}
#     try:
#         if vehicle:
#             pro = vehicleModel.objects.get(pk=int(vehicle)).user
#             users = {pp.user.phone:pp.pk for pp in pro}
#     except:
#         pass
#     return JsonResponse(data=users, safe=False)


@csrf_exempt
def userLogin(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        passw = request.POST.get("password")
        if phone == None or passw == None:
            return JsonResponse({"code": "400", "error": "Invalid details."})
        print(phone)
        users1 = userModel.objects.filter(phone=phone)
        if len(users1) == 0:
            return JsonResponse({"code": "400", "error": "User doesnot exists."})
        else:
            existsession = sessionModel.objects.filter(phone=phone)
            if len(existsession) != 0:
                existsession.delete()
            if check_password(passw, users1[0].passw):
                try:
                    session = sessionModel()
                    tok = os.urandom(32)
                    tok = make_password(tok)
                    session.token = tok
                    session.phone = phone
                    session.tim = datetime.datetime.now()
                    session.save()
                    return JsonResponse(
                        {
                            "code": "200",
                            "data": {
                                "sessionId": tok,
                                "user": userSerializer(users1[0]).data,
                            },
                        }
                    )
                except Exception as e:
                    print(e)
                    return JsonResponse(
                        {"code": "500", "error": "something went wrong."}
                    )
            else:
                return JsonResponse({"code": "400", "error": "Password wrong."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


##########################################################################################################


@csrf_exempt
def userLogout(request):
    if request.method == "POST":
        sessionId = request.POST.get("sessionId")
        if sessionId == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})
        if isauth(sessionId):
            try:
                sessionModel.objects.filter(token=sessionId).delete()
                return JsonResponse({"code": "200", "data": "success"})
            except:
                return JsonResponse({"code": "500", "error": "something went wrong."})
        else:
            return JsonResponse({"code": "401", "error": "Not logged in."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})

##########################################################################################################


@csrf_exempt
def userForgotPass(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        otp = request.POST.get("otp")
        passw = request.POST.get("password")
        if phone == None or otp == None or passw == None:
            return JsonResponse({"code": "500", "error": "Invalid details."})
        try:
            userModel.objects.filter(phone=phone)[0]
        except:
            return JsonResponse({"code": "500", "error": "User not found!"})
        try:
            ot = otpModel.objects.filter(phone=phone)[0]
        except:
            return JsonResponse({"code": "500", "error": "OTP not send yet or expired!"})
        if ot.otp == otp:
            user = userModel.objects.filter(phone=phone)[0]
            print(user)
            user.passw = make_password(passw)
            user.save()
            ot.delete()
            # sendSms("Password changed successfully." , user.phone)
            return JsonResponse({"code": "200", "data": "success"})
        else:
            return JsonResponse({"code": "500", "error": "Incorrect OTP."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})
##########################################################################################################


@csrf_exempt
def userRegister(request):
    firstName = request.POST.get("firstName")
    lastName = request.POST.get("lastName")
    gender = request.POST.get("gender")
    phone = request.POST.get("phone")
    mail = request.POST.get("mail")
    passw = request.POST.get("password")
    img = request.FILES.get("photo")

    if (
        firstName == None
        or lastName == None
        or gender == None
        or phone == None
        or mail == None
        or passw == None
    ):
        return JsonResponse({"code": "400", "error": "Invalid details."})

    c1 = Q(email=mail)
    c2 = Q(phone=phone)

    temp = userModel.objects.filter(c1 | c2)

    if len(temp) == 0:
        try:
            tea = userModel()
            tea.firstName = firstName
            tea.lastName = lastName
            tea.passw = make_password(passw)
            tea.email = mail
            tea.phone = phone
            tea.gender = gender
            tea.dateOfRegistration = datetime.date.today()
            if img:
                tea.photo = img
            tea.save()
            session = sessionModel()
            tok = os.urandom(32)
            tok = make_password(tok)
            session.token = tok
            session.phone = phone
            session.tim = datetime.datetime.now()
            session.save()

            return JsonResponse({"code": "200", "data": {
                                "sessionId": tok,
                                "user": userSerializer(tea).data,
                                }})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "something went wrong."})
    else:
        return JsonResponse({"code": "400", "error": "Email or phone number already taken."})

##########################################################################################################


@csrf_exempt
def userProfile(request):
    sessionId = request.POST.get("sessionId")

    if isauth(sessionId):
        try:
            use = getuser(sessionId).id
            tea = userModel.objects.filter(id=use)
            if not len(tea):
                return JsonResponse({"code": "400", "error": "user not found."})
            tea = userSerializer(tea[0]).data
            return JsonResponse(
                {
                    "code": "200",
                    "data": tea,
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})

##########################################################################################################


@csrf_exempt
def userEditProfile(request):
    sessionId = request.POST.get("sessionId")
    gender = request.POST.get("gender")
    firstName = request.POST.get("firstName")
    lastName = request.POST.get("lastName")
    passw = request.POST.get("password")
    mail = request.POST.get("mail")
    file = request.FILES.get("photo")

    if sessionId == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            ide = getuser(sessionId).id
            tea = userModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Player not found."})
            tea = userModel.objects.get(id=ide)
            if gender:
                tea.gender = gender
            if firstName:
                tea.firstName = firstName
            if lastName:
                tea.lastName = lastName
            if mail:
                tea.email = mail
            if passw:
                tea.passw = make_password(passw)
            if file:
                tea.photo = file
            tea.save()
            te = userSerializer(tea).data
            return JsonResponse({"code": "200", "data": te})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "something went wrong."})

    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################


@csrf_exempt
def userSendOtp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        if phone == None:
            return JsonResponse({"code": "400", "error": "Invalid details."})
        user = userModel.objects.filter(phone=phone)
        if (user):
            return JsonResponse({"code": "400", "error": "user already exist"})
        ot = otpModel.objects.filter(phone=phone)
        if ot:
            ot[0].delete()
        # phone = user[0].phone
        otp = str(createotp())
        mestring = "Your OTP for RoadWings is " + otp
        try:
            res = sendMess(phone, mestring)
            if res == 'success':
                otpmod = otpModel()
                otpmod.otp = otp
                otpmod.phone = phone
                otpmod.save()
                return JsonResponse({"code": "200", "data": "success"})
            else:
                return JsonResponse({"code": "500", "error": res})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "something went wrong."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def userForgotSendOtp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        if phone == None:
            return JsonResponse({"code": "400", "error": "Invalid details."})

        ot = otpModel.objects.filter(phone=phone)
        if ot:
            ot[0].delete()
        # phone = user[0].phone
        otp = str(createotp())
        mestring = "Your OTP for RoadWings is " + otp
        try:
            res = sendMess(phone, mestring)
            if res == 'success':
                otpmod = otpModel()
                otpmod.otp = otp
                otpmod.phone = phone
                otpmod.save()
                return JsonResponse({"code": "200", "data": "success"})
            else:
                return JsonResponse({"code": "500", "error": res})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "something went wrong."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


@csrf_exempt
def userCheckOtp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        otp = request.POST.get("otp")
        if phone == None or otp == None:
            return JsonResponse({"code": "400", "error": "Invalid details."})
        # try:
        #     userModel.objects.filter(phone=phone)[0]
        # except:
        #     return JsonResponse({"code": "400", "error": "User not found!"})
        try:
            ot = otpModel.objects.filter(phone=phone)[0]
        except:
            return JsonResponse(
                {"code": "400", "error": "OTP not send yet or expired!"}
            )
        if ot.otp == otp:
            ot.delete()
            return JsonResponse({"code": "200", "data": "success"})
        else:
            return JsonResponse({"code": "400", "error": "Incorrect OTP."})
    else:
        return JsonResponse({"code": "400", "error": "Method not allowed"})


##########################################################################################################


@csrf_exempt
def userCreateVehicle(request):
    sessionId = request.POST.get("sessionId")
    brand = request.POST.get("brand")
    model = request.POST.get("model")
    color = request.POST.get("color")
    licensePlateNo = request.POST.get("licensePlateNo")
    bluebookPhoto = request.FILES.get("bluebookPhoto")
    bluebookRenewalDate = request.POST.get("bluebookRenewalDate")
    bluebookExpiryDate = request.POST.get("bluebookExpiryDate")
    bluebookOwnerName = request.POST.get("bluebookOwnerName")

    # print(bluebookPhoto)

    if brand == None or model == None or color == None or licensePlateNo == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = vehicleModel()
            tea.brand = brand
            tea.model = model
            tea.color = color
            tea.licensePlateNumber = licensePlateNo
            if bluebookExpiryDate:
                tea.blueBookExpiryDate = bluebookExpiryDate
            if bluebookOwnerName:
                tea.blueBookOwnerName = bluebookOwnerName
            if bluebookPhoto:
                tea.blueBookPhoto = bluebookPhoto
            if bluebookRenewalDate:
                tea.blueBookRenewalDate = bluebookRenewalDate
            tea.user = getuser(sessionId)
            tea.save()
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})

##########################################################################################################


@csrf_exempt
def userEditVehicle(request):
    sessionId = request.POST.get("sessionId")
    brand = request.POST.get("brand")
    model = request.POST.get("model")
    color = request.POST.get("color")
    licensePlateNo = request.POST.get("licensePlateNo")
    bluebookRenewalDate = request.POST.get("bluebookRenewalDate")
    bluebookExpiryDate = request.POST.get("bluebookExpiryDate")
    bluebookOwnerName = request.POST.get("bluebookOwnerName")
    ide = request.POST.get("vehicleId")

    bluebookPhoto = request.FILES.get("bluebookPhoto")

    if brand == None or model == None or color == None or licensePlateNo == None or ide == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        # try:
            tea = vehicleModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Vehicle not found."})
            if bluebookPhoto:
                print('found')
                print(bluebookPhoto)
                tea[0].blueBookPhoto = bluebookPhoto
                tea[0].save()
                
            if tea[0].brand != brand:
                tea.update(brand=brand)
            if tea[0].model != model:
                tea.update(model=model)
            if tea[0].color != color:
                tea.update(color=color)
            if tea[0].licensePlateNumber != licensePlateNo:
                tea.update(licensePlateNumber=licensePlateNo)
            if bluebookRenewalDate:
                if tea[0].blueBookRenewalDate != bluebookRenewalDate:
                    tea.update(blueBookRenewalDate=bluebookRenewalDate)
            if bluebookExpiryDate:
                if tea[0].blueBookExpiryDate != bluebookExpiryDate:
                    tea.update(blueBookExpiryDate=bluebookExpiryDate)
            if bluebookOwnerName:
                if tea[0].blueBookOwnerName != bluebookOwnerName:
                    tea.update(blueBookOwnerName=bluebookOwnerName)
            

            return JsonResponse({"code": "200", "data": "success"})
        # except Exception as e:
        #     print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################

@csrf_exempt
def userDeleteVehicle(request):
    sessionId = request.POST.get("sessionId")
    ide = request.POST.get("vehicleId")
    if ide == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = vehicleModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Vehicle not found."})
            tea.delete()
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################


@csrf_exempt
def userVehicle(request):
    sessionId = request.POST.get("sessionId")
    # filterName = request.POST.get("filterName")
    # page = request.POST.get("page")
    # itemsPerPage = request.POST.get("itemsPerPage")
    if sessionId == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    # if page == 0:
    #     return JsonResponse({"code": "400", "error": "Error page number."})

    if isauth(sessionId):
        try:
            user = getuser(sessionId)
            tea = vehicleModel.objects.filter(
                user=user).order_by("brand")
            if len(tea) == 0:
                return JsonResponse({"code": "200", "totalPages": 1, "data": []})
            tea = vehicleSerializer(tea, many=True).data
            return JsonResponse(
                {
                    "code": "200",
                    "data": tea,
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})
##########################################################################################################
##########################################################################################################
##########################################################################################################


@csrf_exempt
def userCreateAddress(request):
    sessionId = request.POST.get("sessionId")
    city = request.POST.get("city")
    name = request.POST.get("name")
    province = request.POST.get("province")
    address = request.POST.get("address")

    if city == None or province == None or address == None or sessionId == None or name == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = addressModel()
            tea.city = city
            tea.name = name
            tea.address = address
            tea.province = province
            tea.user = getuser(sessionId)
            user = getuser(sessionId)
            tea.save()
            user.address.add(tea.id)
            tea.save()
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})

##########################################################################################################


@csrf_exempt
def userEditAddress(request):
    sessionId = request.POST.get("sessionId")
    city = request.POST.get("city")
    name = request.POST.get("name")
    province = request.POST.get("province")
    address = request.POST.get("address")
    ide = request.POST.get("addressId")

    if city == None or province == None or address == None or sessionId == None or ide == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = addressModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Address not found."})
            if tea[0].city != city:
                tea.update(city=city)
            if tea[0].name != name:
                tea.update(name=name)
            if tea[0].province != province:
                tea.update(province=province)
            if tea[0].address != address:
                tea.update(address=address)
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################

@csrf_exempt
def userDeleteAddress(request):
    sessionId = request.POST.get("sessionId")
    ide = request.POST.get("addressId")
    if ide == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = addressModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Address not found."})
            user = getuser(sessionId)
            user.address.remove(tea[0].id)
            user.save()
            tea[0].deleteStatus = True
            tea[0].save()
            # tea.delete()
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################


@csrf_exempt
def userAddress(request):
    sessionId = request.POST.get("sessionId")

    if sessionId == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            user = getuser(sessionId)
            tea = addressModel.objects.filter(
                user=user).order_by("city")
            if len(tea) == 0:
                return JsonResponse({"code": "200", "totalPages": 1, "data": []})

            tea = addressSerializer(tea, many=True).data
            return JsonResponse(
                {
                    "code": "200",
                    "data": tea,
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################
##########################################################################################################
##########################################################################################################


@csrf_exempt
def userCreateService(request):
    sessionId = request.POST.get("sessionId")
    vehicle = request.POST.get("vehicleId")
    dateo = request.POST.get("dateOfService")
    # address = request.POST.get("addressId")
    dropLocation = request.POST.get("dropLocation")
    pickUpLocation = request.POST.get("pickUpLocation")
    permission_classes = [IsAuthenticated,]
    # def post(self, request, format = None):
    #     user = {}
    #     if vehicle:
    #         users = vehicleModel.objects.get(model = vehicle).users.all()
    #         user = {p.model: p.id for p in users }
    #     return JsonResponse(data = user, safe=False)

    if pickUpLocation == None or dropLocation == None or vehicle == None or dateo == None or sessionId == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            veh = vehicleModel.objects.filter(id=vehicle)
            if not len(veh):
                return JsonResponse({"code": "400", "error": "Invalid vehicle id."})
            # add = addressModel.objects.filter(id=address)
            # if not len(add):
            #     return JsonResponse({"code": "400", "error": "Invalid address id."})

            tea = serviceLogModel()
            tea.vehicle = veh[0]
            tea.pickUpLocation = pickUpLocation
            tea.dropLocation = dropLocation
            tea.user = veh[0].user
            # tea.address = add[0]
            tea.dateOfMaintanance = dateo
            tea.save()
            # send_mail(
            #     'New Service Request',
            #     'You have got a  new service request.',
            #     '3dprintnepal@gmail.com',
            #     ['3dprintnepal@gmail.com'],
            #     fail_silently=False,
            # )
            messages.success(request, "Service Record Added Succesfully")

            return JsonResponse({"code": "200", "data": "success"})
        
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})

##########################################################################################################


@csrf_exempt
def userEditService(request):
    sessionId = request.POST.get("sessionId")
    vehicle = request.POST.get("vehicleId")
    dateo = request.POST.get("dateOfService")
    # address = request.POST.get("addressId")
    ide = request.POST.get("serviceId")
    dropLocation = request.POST.get("dropLocation")
    pickUpLocation = request.POST.get("pickUpLocation")
    if pickUpLocation == None or dropLocation == None or vehicle == None or dateo == None or sessionId == None or ide == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = serviceLogModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Service log not found."})
            veh = vehicleModel.objects.filter(id=vehicle)
            if not len(veh):
                return JsonResponse({"code": "400", "error": "Invalid vehicle id."})
            # add = addressModel.objects.filter(id=address)
            # if not len(add):
            #     return JsonResponse({"code": "400", "error": "Invalid address id."})

            if tea[0].vehicle != vehicle:
                tea.update(vehicle=veh[0])
            if tea[0].dropLocation != dropLocation:
                tea.update(dropLocation=dropLocation)
            if tea[0].pickUpLocation != pickUpLocation:
                tea.update(pickUpLocation=pickUpLocation)
            # if tea[0].address != address:
            #     tea.update(address=add)
            if tea[0].dateOfMaintanance != dateo:
                tea.update(dateOfMaintanance=dateo)
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################

@csrf_exempt
def userDeleteService(request):
    sessionId = request.POST.get("sessionId")
    ide = request.POST.get("serviceId")
    if ide == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            tea = serviceLogModel.objects.filter(id=ide)
            if len(tea) == 0:
                return JsonResponse({"code": "400", "error": "Service log not found."})
            tea.delete()
            return JsonResponse({"code": "200", "data": "success"})
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################


@csrf_exempt
def userService(request):
    sessionId = request.POST.get("sessionId")
    if sessionId == None:
        return JsonResponse({"code": "400", "error": "Invalid details."})
    if isauth(sessionId):
        try:
            user = getuser(sessionId)
            tea = serviceLogModel.objects.filter(
                user=user).order_by("-dateOfMaintanance")
            if len(tea) == 0:
                return JsonResponse({"code": "200", "totalPages": 1, "data": []})

            tea = serviceLogSerializer(tea, many=True).data
            return JsonResponse(
                {
                    "code": "200",
                    "data": tea,
                }
            )
        except Exception as e:
            print(e)
            return JsonResponse({"code": "500", "error": "Something went wrong."})
    else:
        return JsonResponse({"code": "401", "error": "Not logged in."})


##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


def createotp():
    value = randint(100000, 999999)
    otps = otpModel.objects.filter(otp=value)
    if otps:
        createotp()
    else:
        return value


def isauth(sessionId):
    session = sessionModel.objects.filter(token=sessionId)
    if len(session) != 0:
        return True
    else:
        return False


def getuser(sessionId):
    session = sessionModel.objects.filter(token=sessionId)
    # print(sessionId, session)
    if len(session) != 0:
        return userModel.objects.filter(phone=session[0].phone)[0]
    else:
        return ""


def sendMess(phone, mess):
    auth_token = settingsModel.objects.all()[0].sms_token
    data = {'auth_token': auth_token, 'to': phone, 'text': mess}
    url = 'https://sms.aakashsms.com/sms/v3/send/'
    res = requests.post(url, data=data)
    res = res.json()
    print(res)
    if res['error']:
        return res['message']
    else:
        return 'success'
