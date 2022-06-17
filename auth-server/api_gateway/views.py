from rest_framework_simplejwt.authentication import JWTAuthentication
from djproxy.views import HttpProxy
from django.conf import settings


class VerifyToken:
    authenticator = JWTAuthentication()
    """
    인증
    """

    def process_request(self, proxy, request, **kwargs):
        response = self.authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user, token = response
            kwargs['headers']['Remote-User'] = str(user.id)
        else:
            kwargs['headers']['Remote-User'] = '1'  # TODO Temp
        return kwargs


class UserAPIView(HttpProxy):
    base_url = getattr(settings, 'USER_API_BASE_URL')
    reverse_urls = [
        ('/user/', getattr(settings, 'USER_API_BASE_URL'))
    ]
    proxy_middleware = [
        'djproxy.proxy_middleware.AddXFF',
        'djproxy.proxy_middleware.AddXFH',
        'djproxy.proxy_middleware.AddXFP',
        'djproxy.proxy_middleware.ProxyPassReverse',
        'api_gateway.views.VerifyToken',
    ]


class SearchAPIView(HttpProxy):
    base_url = getattr(settings, 'SEARCH_API_BASE_URL')
    reverse_urls = [
        ('/search/', getattr(settings, 'SEARCH_API_BASE_URL'))
    ]
    proxy_middleware = [
        'djproxy.proxy_middleware.AddXFF',
        'djproxy.proxy_middleware.AddXFH',
        'djproxy.proxy_middleware.AddXFP',
        'djproxy.proxy_middleware.ProxyPassReverse',
        'api_gateway.views.VerifyToken'
    ]
