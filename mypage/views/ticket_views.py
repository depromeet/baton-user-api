from mypage.models import Bookmark
from mypage.serializers import ticket_serializers as serializers

from rest_framework import generics


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
