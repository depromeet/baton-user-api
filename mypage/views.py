from mypage.models import User
from mypage.serializers import UserSerializer, TicketListSerializer, BuySerializer, BookmarkSerializer

from rest_framework import generics
from django.shortcuts import get_object_or_404


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
    serializer_class = TicketListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        return user.sell_tickets


class BuyView(generics.ListAPIView):
    """
    구매내역
    """
    serializer_class = BuySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        return user.buys


class BookmarkView(generics.ListAPIView):
    """
    관심상품
    """
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        return user.bookmarks
