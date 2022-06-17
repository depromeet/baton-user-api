from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView
from accounts.views import *


urlpatterns = [
    path('login/kakao', KakaoLoginView.as_view(), name='kakao-login'),
    path('socialusers', SocialUserCreateView.as_view(), name='socialuser-create'),
    path('socialusers/<int:pk>', SocialUserDeleteView.as_view(), name='socialuser-delete'),

    path('accounts/kakao', kakao_login, name='kakao'),  # TODO temp
    path('accounts/kakao/callback', kakao_callback, name='kakao-callback'),  # TODO temp

    path('token/verify', TokenVerifyView.as_view(), name='token-verify'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
