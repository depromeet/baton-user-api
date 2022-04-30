from mypage.models import User
from mypage.serializers import UserSerializer, TicketListSerializer, BuySerializer, BookmarkSerializer

from rest_framework import generics
from rest_framework.response import Response


class UserDetailView(generics.RetrieveAPIView):
    """
    마이페이지
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellView(generics.ListAPIView):
    """
    판매내역
    """
    queryset = User.objects.all()
    serializer_class = TicketListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_object().sell_tickets

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BuyView(generics.ListAPIView):
    """
    구매내역
    """
    queryset = User.objects.all()
    serializer_class = BuySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_object().buys

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookmarkView(generics.ListAPIView):
    """
    관심상품
    """
    queryset = User.objects.all()
    serializer_class = BookmarkSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_object().bookmarks

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)