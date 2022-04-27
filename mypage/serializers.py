from rest_framework import serializers
from mypage.models import Ticket, Buy


class TicketListSerializer(serializers.ModelSerializer):
    """
    Ticket list 나올 때 한 티켓에 나타나는 정보
    """
    class Meta:
        model = Ticket
        fields = ['id', 'state', 'location', 'price', 'created_at']  # TODO 필드 추가


class BuySerializer(serializers.ModelSerializer):
    """
    구매내역 (구매 날짜 + 양도권)
    """
    ticket = TicketListSerializer()

    class Meta:
        model = Buy
        fields = ['id', 'date', 'ticket']
