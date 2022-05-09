from accounts.serializers import KaKaoLoginSerializer
from accounts.models import SocialUser
from mypage.models import User as AppUser

import requests
from urllib.parse import urlencode
from json.decoder import JSONDecodeError
from django.http import JsonResponse

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


BASE_URL = 'http://127.0.0.1:8000/'


def kakao_login(request):  # TODO 프론트에서 담당
    authorize_url = "https://kauth.kakao.com/oauth/authorize"

    query_kwargs = {
        'client_id': getattr(settings, 'KAKAO_REST_API_KEY'),
        'redirect_uri': BASE_URL + reverse('accounts:kakao-callback'),
        'response_type': 'code',
    }
    return redirect(f'{authorize_url}?{urlencode(query_kwargs)}')


def kakao_callback(request):  # TODO 프론트에서 담당
    access_token_url = "https://kauth.kakao.com/oauth/token"

    query_kwargs = {
        'grant_type': 'authorization_code',
        'client_id': getattr(settings, 'KAKAO_REST_API_KEY'),
        'redirect_uri': BASE_URL + reverse('accounts:kakao-callback'),
        'code': request.GET.get("code"),
    }

    token_resp = requests.get(f'{access_token_url}?{urlencode(query_kwargs)}')
    token_resp_json = token_resp.json()
    error = token_resp_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    # access_token = token_resp_json.get("access_token")
    return JsonResponse(token_resp_json)


class KakaoLoginView(GenericAPIView):
    serializer_class = KaKaoLoginSerializer
    provider = 'kakao'

    def get_app_user(self, uid):
        """
        소셜 서비스 인증 서버에서 받은 uid를 이용해 app user 객체를 추출하고,
        없으면 생성하여 반환
        """
        try:
            social_user = SocialUser.objects.get(provider=self.provider, uid=uid)
            return social_user.app_user
        except SocialUser.DoesNotExist:  # 신규 회원일 때
            social_user = SocialUser.objects.create_user(provider=self.provider, uid=uid)
            app_user = AppUser.objects.create(social_user=social_user)
            return app_user

    # def login(self):
    #     """
    #     Access Token 발행
    #     """
    #     self.user = self.serializer.validated_data['user']
    #     self.token = create_token(token_model, self.user, self.serializer)

    def post(self, request):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data['id']
        app_user = self.get_app_user(uid)
        # self.login(app_user)
        # return self.get_response()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)  # TODO 수정
