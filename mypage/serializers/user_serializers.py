from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


class TicketListSerializer(serializers.ModelSerializer):
    """
    Ticket list 나올 때 한 티켓에 나타나는 정보
    """

    class Meta:
        model = Ticket
        fields = ['id', 'state', 'location', 'price', 'created_at']  # TODO 필드 추가
        extra_kwargs = {
            'id': {'help_text': 'Ticket ID'},
        }


class UserBuySerializer(serializers.ModelSerializer):
    """
    구매내역 (구매 날짜 + 양도권)
    """
    ticket = TicketListSerializer()

    class Meta:
        model = Buy
        fields = ['id', 'date', 'ticket']
        extra_kwargs = {
            'id': {'help_text': 'Buy ID'},
        }


class UserBookmarkSerializer(serializers.ModelSerializer):
    """
    관심상품 (bookmark id, tickets)
    """
    ticket = TicketListSerializer()

    class Meta:
        model = Bookmark
        fields = ['id', 'ticket']
        extra_kwargs = {
            'id': {'help_text': 'Bookmark ID'},
        }


class UserSerializer(serializers.ModelSerializer):
    """
    마이페이지 사용자 정보
    """
    sells = serializers.HyperlinkedIdentityField(view_name='mypage:user-sell', help_text='판매내역 URL')
    buys = serializers.HyperlinkedIdentityField(view_name='mypage:user-buy', help_text='구매 및 예약내역 URL')
    bookmarks = serializers.HyperlinkedIdentityField(view_name='mypage:user-bookmark', help_text='관심상품 URL')

    class Meta:
        model = User
        fields = ['nickname', 'sells', 'buys', 'bookmarks']  # TODO 로그아웃, 회원탈퇴 추가
