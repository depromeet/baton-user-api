from rest_framework.authentication import RemoteUserAuthentication as BaseRemoteUserAuthentication


class RemoteUserAuthentication(BaseRemoteUserAuthentication):
    header = "HTTP_REMOTE_USER"
