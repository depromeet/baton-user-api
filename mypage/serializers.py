from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


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


class BookmarkSerializer(serializers.ModelSerializer):
    """
    관심상품 (bookmark id, tickets)
    """
    ticket = TicketListSerializer()

    class Meta:
        model = Bookmark
        fields = ['id', 'ticket']


class UserSerializer(serializers.ModelSerializer):
    """
    마이페이지 사용자 정보
    """
    sells = serializers.HyperlinkedIdentityField(view_name='mypage:user-sell')
    buys = serializers.HyperlinkedIdentityField(view_name='mypage:user-buy')
    bookmarks = serializers.HyperlinkedIdentityField(view_name='mypage:user-bookmark')

    class Meta:
        model = User
        fields = ['nickname', 'sells', 'buys', 'bookmarks']  # TODO 로그아웃, 회원탈퇴 추가
