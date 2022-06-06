from .models import User, Account

from rest_framework import serializers

from django.contrib.auth import get_user_model
# from django.contrib.gis.geos import Point


class AccountSerializer(serializers.ModelSerializer):
    """
    계좌정보 수정
    """

    class Meta:
        model = Account
        fields = ['holder', 'bank', 'number']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    회원가입
    """
    id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    account = AccountSerializer(required=False)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'nickname', 'phone_number', 'account',
                  'latitude', 'longitude', 'address', 'detailed_address',
                  'check_terms_of_service', 'check_privacy_policy']

    def create(self, validated_data):
        # reference: https://stackoverflow.com/questions/37240621/django-rest-framework-updating-nested-object
        # create account
        if 'account' in validated_data:
            account_data = validated_data.pop('account')
            account = Account.objects.create(**account_data)
            validated_data['account'] = account

        x = validated_data.pop('longitude')
        y = validated_data.pop('latitude')
        # validated_data['point'] = Point(x, y)

        # create user
        user = User.objects.create(**validated_data)
        return user
