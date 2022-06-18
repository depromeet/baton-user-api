from mypage.models import Bookmark, Buy
from mypage.serializers import ticket_serializers as serializers

from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema

from django.db import connection, transaction


class BuyCreateView(generics.CreateAPIView):
    """
    Reserve a ticket.
    Buy instance 생성 (state 0 -> 1)
    """
    serializer_class = serializers.BuyCreateSerializer

    def perform_create(self, serializer):
        buy = serializer.save()
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE Ticket SET state=1 WHERE id={buy.ticket_id}")
            cursor.fetchone()


class BuyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    구매/예약 상세 조회, 수정, 삭제
    """
    queryset = Buy.objects.all()
    serializer_class = serializers.BuyDetailSerializer

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.ticket.state = 0
        instance.ticket.save()
        instance.delete()

    @swagger_auto_schema(
        responses={200: '삭제가 완료되었습니다.'},
    )
    def delete(self, request, *args, **kwargs):
        """
        Cancel Reservation.
        Buy instance 삭제 (ticket state 1,2 -> 0)
        """
        response = super().delete(request, *args, **kwargs)
        response.data = {'detail': '삭제가 완료되었습니다.'}
        response.status_code = status.HTTP_200_OK
        return response


class BookmarkCreateView(generics.CreateAPIView):
    """
    Bookmark instance 생성
    """
    serializer_class = serializers.BookmarkSerializer

    def perform_create(self, serializer):
        bookmark = serializer.save()
        with connection.cursor() as cursor:
            cursor.execute(f"UPDATE Ticket SET bookmark_count={bookmark.ticket.bookmark_count+1} WHERE id={bookmark.ticket_id}")
            cursor.fetchone()


class BookmarkDetailView(generics.RetrieveDestroyAPIView):
    """
    Bookmark instance 상세, 삭제
    """
    queryset = Bookmark.objects.all()
    serializer_class = serializers.BookmarkSerializer

    @swagger_auto_schema(
        responses={200: '삭제가 완료되었습니다.'},
    )
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        response.data = {'detail': '삭제가 완료되었습니다.'}
        response.status_code = status.HTTP_200_OK
        return response

    @transaction.atomic
    def perform_destroy(self, instance):
        instance.ticket.bookmark_count -= 1
        instance.ticket.save()
        instance.delete()
