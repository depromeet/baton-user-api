from django.urls import path
from accounts.views import *

app_name = 'accounts'


urlpatterns = [
    path('login/kakao', KakaoLoginView.as_view(), name='kakao-login'),
    # path('signup/kakao')
    path('accounts/kakao', kakao_login, name='kakao'),  # TODO temp
    path('accounts/kakao/callback', kakao_callback, name='kakao-callback'),  # TODO temp
]
