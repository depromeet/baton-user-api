from rest_framework import serializers
from mypage.models import Ticket, Bookmark, Buy, User


class TicketListSerializer(serializers.ModelSerializer):
    """
    Ticket list 나올 때 한 티켓에 나타나는 정보
    """
    id = serializers.IntegerField(help_text='Ticket ID')
    state = serializers.IntegerField(help_text='양도권 상태 (0: 판매중, 1: 예약중, 2: 판매완료)')
    class Meta:
        model = Ticket
        fields = ['id', 'state', 'location', 'price', 'created_at']  # TODO 필드 추가


class UserBuySerializer(serializers.ModelSerializer):
    """
    구매내역 (구매 날짜 + 양도권)
    """
    id = serializers.IntegerField(help_text='Buy ID')
    date = serializers.DateTimeField(help_text='구매일시')
    ticket = TicketListSerializer(help_text='Ticket list 나올 때 한 티켓에 나타나는 정보')

    class Meta:
        model = Buy
        fields = ['id', 'date', 'ticket']


class UserBookmarkSerializer(serializers.ModelSerializer):
    """
    관심상품 (bookmark id, tickets)
    """
    id = serializers.IntegerField(help_text='Bookmark ID')
    ticket = TicketListSerializer(help_text='Ticket list 나올 때 한 티켓에 나타나는 정보')

    class Meta:
        model = Bookmark
        fields = ['id', 'ticket']


class UserSerializer(serializers.ModelSerializer):
    """
    마이페이지 사용자 정보
    """
    sells = serializers.HyperlinkedIdentityField(view_name='mypage:user-sell', help_text='판매내역')
    buys = serializers.HyperlinkedIdentityField(view_name='mypage:user-buy', help_text='구매 및 예약내역')
    bookmarks = serializers.HyperlinkedIdentityField(view_name='mypage:user-bookmark', help_text='관심상품')

    class Meta:
        model = User
        fields = ['nickname', 'sells', 'buys', 'bookmarks']  # TODO 로그아웃, 회원탈퇴 추가
