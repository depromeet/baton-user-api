from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


class BuyCreateSerializer(serializers.ModelSerializer):
    """
    Create Buy instance
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), help_text='User ID(integer)')
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), help_text='Ticket ID')

    class Meta:
        model = Buy
        fields = ['id', 'user', 'ticket', 'date']
        extra_kwargs = {
            'id': {'help_text': 'Buy ID'},
        }


class BuyDetailSerializer(serializers.ModelSerializer):
    """
    Buy instance
    """
    user = serializers.PrimaryKeyRelatedField(read_only=True, help_text='User ID(integer)')
    ticket = serializers.PrimaryKeyRelatedField(read_only=True, help_text='Ticket ID')

    class Meta:
        model = Buy
        fields = ['id', 'user', 'ticket', 'date']
        extra_kwargs = {
            'id': {'help_text': 'Buy ID'},
            'data': {'required': True},
        }


class BookmarkSerializer(serializers.ModelSerializer):
    """
    Bookmark instance
    """
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), help_text='User ID(integer)')
    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all(), help_text='Ticket ID')

    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'ticket']
        extra_kwargs = {
            'id': {'help_text': 'Bookmark ID'},
        }
