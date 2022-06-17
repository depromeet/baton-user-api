from accounts.jwt_serializers import TokenObtainPairSerializer
from accounts.models import SocialUser

from rest_framework import status
from rest_framework.response import Response

from django.db import IntegrityError


class SocialLoginMixin:
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
            serializer.validated_data['provider'] = self.provider
            return Response(data=serializer.validated_data, status=status.HTTP_401_UNAUTHORIZED)
        else:
            token = TokenObtainPairSerializer.get_token(social_user)
            return Response(token, status=status.HTTP_200_OK)

    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            social_user = serializer.save()
        except IntegrityError as error:
            return Response({'detail': error.args[1]}, status=status.HTTP_409_CONFLICT)
            # return JsonResponse({'detail': "이미 존재하는 사용자입니다."}, status=status.HTTP_409_CONFLICT)
        else:
            token = TokenObtainPairSerializer.get_token(social_user)
            return Response(token, status=status.HTTP_201_CREATED)


class LogoutMixin:
    pass
