from mypage.models import User
from mypage.serializers import TicketListSerializer

from rest_framework import generics
from rest_framework.response import Response


class BookmarkView(generics.ListAPIView):
    """
    List all tickets marked from a user.
    """
    queryset = User.objects.all()
    serializer_class = TicketListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_object().bookmark_tickets

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
