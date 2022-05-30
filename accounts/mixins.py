from accounts.serializers import JWTSerializer
from accounts.models import SocialUser
from mypage.models import User as AppUser

from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.http import JsonResponse


class SocialLoginMixin:
    def get_user_objects(self, uid):
        """
        소셜 서비스 인증 서버에서 받은 uid를 이용해 social_user 객체를 추출하여 반환.
        새로운 사용자의 경우 social_user와 app_user를 생성.
        """
        try:
            social_user = SocialUser.objects.get(provider=self.provider, uid=uid)
            app_user = social_user.app_user
            return social_user, app_user
        except SocialUser.DoesNotExist:  # 신규 회원일 때
            social_user = SocialUser.objects.create_user(provider=self.provider, uid=uid)
            app_user = AppUser.objects.create(social_user=social_user)
            return social_user, app_user

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

        uid = serializer.validated_data['id']
        social_user, app_user = self.get_user_objects(uid)
        access_token, refresh_token = self.create_token(social_user)

        data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': app_user,
        }
        response_data = JWTSerializer(data).data

        return JsonResponse(response_data, status=status.HTTP_200_OK)


class LogoutMixin:
    pass
