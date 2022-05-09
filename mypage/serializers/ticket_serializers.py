from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


class BuyCreateSerializer(serializers.ModelSerializer):
    """
    Create Buy instance
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Buy
        fields = ['id', 'user', 'ticket', 'date']


class BuyDetailSerializer(serializers.ModelSerializer):
    """
    Buy instance
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    ticket = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.DateTimeField(required=True)

    class Meta:
        model = Buy
        fields = ['id', 'user', 'ticket', 'date']


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmark instance
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'ticket']
