from mypage.models import Bookmark, Buy
from mypage.serializers import ticket_serializers as serializers

from rest_framework import generics


class BuyListView(generics.ListCreateAPIView):
    queryset = Buy.objects.all()
    serializer_class = serializers.BuyCreateSerializer

    def perform_create(self, serializer):
        buy = serializer.save()
        buy.ticket.state = 1
        buy.ticket.save()

    def get(self, request, *args, **kwargs):
        """
        구매/예약 목록
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Reserve a ticket.
        Buy instance 생성 (ticket state 0 -> 1)
        """
        return self.create(request, *args, **kwargs)


class BuyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    구매/예약 상세 조회, 수정, 삭제
    """
    queryset = Buy.objects.all()
    serializer_class = serializers.BuyDetailSerializer

    def perform_destroy(self, instance):
        instance.ticket.state = 0
        instance.ticket.save()
        instance.delete()

    def delete(self, request, *args, **kwargs):
        """
        Cancel Reservation.
        Buy instance 삭제 (ticket state 1,2 -> 0)
        """
        return super().delete(request, *args, **kwargs)


class BookmarkListView(generics.ListCreateAPIView):
    """
    Bookmark instance 목록, 생성
    """
    queryset = Bookmark.objects.all()
    serializer_class = serializers.BookmarkSerializer


class BookmarkDetailView(generics.RetrieveDestroyAPIView):
    """
    Bookmark instance 상세, 삭제
    """
    queryset = Bookmark.objects.all()
    serializer_class = serializers.BookmarkSerializer
