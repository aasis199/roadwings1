from rest_framework import serializers

from api.models import addressModel, notificationLogModel, serviceLogModel, userModel, vehicleModel


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel
        fields = [
            'id',
            'firstName',
            'lastName',
            'email',
            'phone',
            # 'address',
            # 'userType',
            'gender',
            'photo',
            # 'deviceId',
            'phoneStatus',
            'dateOfRegistration'
        ]
        depth = 1


class serviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = serviceLogModel
        fields = [
            'id',
            'dateOfMaintanance',
            'vehicle',
            'invoice',
            'statusType',
            'deleteStatus',
            'pickUpLocation',
            'dropLocation'
        ]
        depth = 1


class notificationSerializer(serializers.ModelSerializer):
    user = userSerializer()

    class Meta:
        model = notificationLogModel
        fields = [
            'id',
            'title',
            'message',
            'file',
            'user'
        ]
        depth = 1


class addressSerializer(serializers.ModelSerializer):
    # user = userSerializer()

    class Meta:
        model = addressModel
        fields = [
            'id',
            'name',
            'province',
            'city',
            'address',
            'deleteStatus',
        ]
        depth = 1


class vehicleSerializer(serializers.ModelSerializer):
    user = userSerializer()

    class Meta:
        model = vehicleModel
        fields = [
            'id',
            'brand',
            'model',
            'color',
            'licensePlateNumber',
            'blueBookPhoto',
            'blueBookRenewalDate',
            'blueBookExpiryDate',
            'blueBookOwnerName',
            'user',
        ]
        depth = 1
