from mypage.models import Bookmark, Buy
from mypage.serializers import ticket_serializers as serializers

from rest_framework import generics, status
from drf_yasg.utils import swagger_auto_schema

from django.db import transaction


class BuyCreateView(generics.CreateAPIView):
    """
    Reserve a ticket.
    Buy instance 생성 (state 0 -> 1)
    """
    serializer_class = serializers.BuyCreateSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        buy = serializer.save()
        buy.ticket.state = 1
        buy.ticket.save()


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

    @transaction.atomic
    def perform_create(self, serializer):
        bookmark = serializer.save()
        bookmark.ticket.bookmark_count += 1
        bookmark.ticket.save()


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
