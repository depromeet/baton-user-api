from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


class BuyCreateSerializer(serializers.ModelSerializer):
    """
    Create Buy instance
    """
    id = serializers.IntegerField(help_text='Buy ID')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), help_text='User ID(integer)')
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), help_text='Ticket ID')
    date = serializers.DateTimeField(help_text='구매일시')

    class Meta:
        model = Buy
        fields = ['id', 'user', 'ticket', 'date']


class BuyDetailSerializer(serializers.ModelSerializer):
    """
    Buy instance
    """
    id = serializers.IntegerField(help_text='Buy ID')
    user = serializers.PrimaryKeyRelatedField(read_only=True, help_text='User ID(integer)')
    ticket = serializers.PrimaryKeyRelatedField(read_only=True, help_text='Ticket ID')
    date = serializers.DateTimeField(required=True, help_text='구매일시')

    class Meta:
        model = Buy
        fields = ['id', 'user', 'ticket', 'date']


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmark instance
    """
    id = serializers.IntegerField(help_text='Bookmark ID')
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), help_text='User ID(integer)')
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), help_text='Ticket ID')

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'ticket']
