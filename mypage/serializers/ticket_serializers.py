from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmark instance
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'ticket']
