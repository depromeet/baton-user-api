from accounts.serializers import JWTSerializer
from accounts.models import SocialUser

from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.http import JsonResponse
from django.db import IntegrityError


class SocialLoginMixin:
    def create_token(self, social_user):
        """
        Access Token 발행
        """
        refresh = TokenObtainPairSerializer.get_token(social_user)
        return str(refresh.access_token), str(refresh)

    def login(self, request):
        """
        Social Service Access Token을 입력 받아, Baton App의 Access Token을 반환
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['uid']
        try:
            social_user = SocialUser.objects.get(provider=self.provider, uid=uid)
        except SocialUser.DoesNotExist:  # 신규 회원일 때 TODO 필드 직접 입력하기, nickname 없을 경우 에러 반환
            return JsonResponse(data=serializer.validated_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            access_token, refresh_token = self.create_token(social_user)
            data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': social_user,
            }
            return JsonResponse(JWTSerializer(data).data, status=status.HTTP_200_OK)

    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            social_user = serializer.save(provider=self.provider)
        except IntegrityError as exc:
            JsonResponse(exc, status=status.HTTP_409_CONFLICT)
        else:
            access_token, refresh_token = self.create_token(social_user)
            data = {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': social_user,
            }
            return JsonResponse(JWTSerializer(data).data, status=status.HTTP_201_CREATED)


class LogoutMixin:
    pass
