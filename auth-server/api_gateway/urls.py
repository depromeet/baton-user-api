from api_gateway import views
from django.urls import re_path


urlpatterns = [
    re_path(r'user/(?P<url>.*)$', views.UserAPIView.as_view(), name='user-api'),
    re_path(r'search/(?P<url>.*)$', views.SearchAPIView.as_view(), name='search-api'),
]

