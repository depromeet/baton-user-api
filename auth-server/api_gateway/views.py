from djproxy.views import HttpProxy
from django.conf import settings


class UserAPIView(HttpProxy):
    base_url = getattr(settings, 'USER_API_BASE_URL')
    reverse_urls = [
        ('/user/', getattr(settings, 'USER_API_BASE_URL'))
    ]


class SearchAPIView(HttpProxy):
    base_url = getattr(settings, 'SEARCH_API_BASE_URL')
    reverse_urls = [
        ('/search/', getattr(settings, 'SEARCH_API_BASE_URL'))
    ]
