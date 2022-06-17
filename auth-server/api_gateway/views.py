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
            # print("this is decoded token claims", token.payload)
            kwargs['headers']['REMOTE_USER'] = str(user.id)
        else:
            kwargs['headers']['REMOTE_USER'] = '1'  # TODO Temp
        return kwargs

    # def process_response(self, proxy, request, upstream_response, response):
    #     """Modify the HttpResponse object before sending it downstream.
    #
    #     proxy - the HttpProxy instance calling thid method
    #     request - a DownstreamRequest wrapper for the django request
    #     upstream_response - the response object resulting from requesting the
    #                         proxied endpoint
    #     response - the django HttpResponse object to be send downstream
    #
    #     Returns a modified django HttpResponse object that is then sent to
    #     the end user.
    #
    #     """
    #     pass


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
