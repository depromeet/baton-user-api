from rest_framework import serializers
from mypage.models import Ticket


class TicketListSerializer(serializers.ModelSerializer):
    """
    Ticket list 나올 때 한 티켓에 나타나는 정보
    """
    class Meta:
        model = Ticket
        fields = ['id', 'price']  # TODO 필드 추가
