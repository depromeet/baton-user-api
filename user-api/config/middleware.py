from django.contrib.auth.middleware import RemoteUserMiddleware as BaseRemoteUserMiddleware


class RemoteUserMiddleware(BaseRemoteUserMiddleware):
    header = 'HTTP_REMOTE_USER'
