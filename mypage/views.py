from mypage.models import User
from mypage.serializers import UserSerializer, TicketListSerializer, BuySerializer, BookmarkSerializer

from rest_framework import generics
from django.http import Http404
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
        state = self.request.query_params.get('state', '0')
        if state not in {'0', '2'}:
            raise Http404('Ticket state value error.')
        return user.sell_tickets.filter(state=state)


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
        state = self.request.query_params.get('state')
        if state:
            if state in {'0', '1', '2'}:
                return user.bookmarks.filter(ticket__state=state)
            else:
                raise Http404('Ticket state value error.')
        return user.bookmarks

