from django.urls import path
from accounts.views import *

app_name = 'accounts'


urlpatterns = [
    path('login/kakao', KakaoLoginView.as_view(), name='kakao-login'),
    path('signup/<str:provider>', SocialUserCreateView.as_view(), name='signup'),
    path('socialusers/<int:pk>', SocialUserDeleteView.as_view(), name='socialuser-delete'),
    path('accounts/kakao', kakao_login, name='kakao'),  # TODO temp
    path('accounts/kakao/callback', kakao_callback, name='kakao-callback'),  # TODO temp
]
