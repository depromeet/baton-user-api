from accounts.serializers import KaKaoLoginSerializer
from accounts.mixins import SocialLoginMixin, LogoutMixin

from rest_framework.generics import GenericAPIView

import requests
from urllib.parse import urlencode
from json.decoder import JSONDecodeError
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

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


class SocialLoginView(GenericAPIView, SocialLoginMixin):
    def post(self, request):
        return self.login(request)


class KakaoLoginView(SocialLoginView):
    serializer_class = KaKaoLoginSerializer
    provider = 'kakao'


class LogoutView(GenericAPIView, LogoutMixin):
    pass
