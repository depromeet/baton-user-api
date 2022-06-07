from rest_framework import serializers

from django.contrib.auth import get_user_model
# from django.contrib.gis.geos import Point


class AccountSerializer(serializers.Serializer):
    """
    계좌정보 수정
    """
    holder = serializers.CharField(help_text='예금주')
    bank = serializers.CharField(help_text='은행')
    number = serializers.CharField(help_text='계좌번호')


class UserCreateSerializer(serializers.Serializer):
    """
    회원가입
    """
    # id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    name = serializers.CharField()
    nickname = serializers.CharField()
    phone_number = serializers.CharField()
    account = AccountSerializer(required=False)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    address = serializers.CharField()
    detailed_address = serializers.CharField()
    check_terms_of_service = serializers.BooleanField()
    check_privacy_policy = serializers.BooleanField()
