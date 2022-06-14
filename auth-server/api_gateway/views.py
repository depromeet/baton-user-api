from djproxy.views import HttpProxy
# from revproxy.views import ProxyView

from django.conf import settings


# class UserAPIView(ProxyView):
#     # upstream = 'baton-user-api.baton.svc.cluster.local'
#     upstream = getattr(settings, 'USER_API_BASE_URL')
#     # upstream = 'https://baton.yonghochoi.com/'
#     default_content_type = 'application/json'


class UserAPIView(HttpProxy):
    base_url = 'http://host.docker.internal:8000/user/'
    reverse_urls = [
        ('/user/', 'http://host.docker.internal:8000/user/')
    ]


class SearchAPIView(HttpProxy):
    base_url = 'https://baton.yonghochoi.com/search/'
    reverse_urls = [
        ('/search/', 'https://baton.yonghochoi.com/search/')
    ]
