from mypage.models import Bookmark, Buy
from mypage.serializers import ticket_serializers as serializers

from rest_framework import generics


class BuyCreateView(generics.CreateAPIView):
    """
    Reserve a ticket.
    Buy instance 생성 (state 0 -> 1)
    """
    serializer_class = serializers.BuyCreateSerializer

    def perform_create(self, serializer):
        buy = serializer.save()
        buy.ticket.state = 1
        buy.ticket.save()


class BuyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Cancel Reservation.
    Buy instance 삭제 (state 1,2 -> 0)
    """
    queryset = Buy.objects.all()
    serializer_class = serializers.BuyDetailSerializer

    def perform_destroy(self, instance):
        instance.ticket.state = 0
        instance.ticket.save()
        instance.delete()


class BookmarkCreateView(generics.CreateAPIView):
    """
    Bookmark instance 생성
    """
    serializer_class = serializers.BookmarkSerializer


class BookmarkDestroyView(generics.DestroyAPIView):
    """
    Bookmark instance 삭제
    """
    queryset = Bookmark.objects.all()
    serializer_class = serializers.BookmarkSerializer
