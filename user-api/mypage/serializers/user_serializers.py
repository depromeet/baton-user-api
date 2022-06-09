from mypage.models import Ticket, Bookmark, Buy, User, Account

from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point


class AccountSerializer(serializers.ModelSerializer):
    """
    계좌정보 수정
    """

    class Meta:
        model = Account
        fields = ['holder', 'bank', 'number']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    회원가입
    """
    id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    # id = serializers.IntegerField()
    account = AccountSerializer(required=False)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'nickname', 'phone_number', 'account',
                  'latitude', 'longitude', 'address', 'detailed_address',
                  'check_terms_of_service', 'check_privacy_policy']

    def create(self, validated_data):
        # reference: https://stackoverflow.com/questions/37240621/django-rest-framework-updating-nested-object
        # create account
        if 'account' in validated_data:
            account_data = validated_data.pop('account')
            account = Account.objects.create(**account_data)
            validated_data['account'] = account

        latitude = validated_data.pop('latitude')
        longitude = validated_data.pop('longitude')
        validated_data['point'] = Point(longitude, latitude, srid=4326)

        # create user
        user = User.objects.create(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    마이페이지 사용자 정보
    """
    account = AccountSerializer()
    latitude = serializers.FloatField(source='point.x')
    longitude = serializers.FloatField(source='point.y')

    class Meta:
        model = User
        fields = ['id', 'name', 'nickname', 'phone_number', 'created_on', 'account',
                  'latitude', 'longitude', 'address', 'detailed_address', ]


class TicketListSerializer(serializers.ModelSerializer):
    """
    Ticket list 나올 때 한 티켓에 나타나는 정보
    """
    mainImage = serializers.CharField(source='main_image')
    createAt = serializers.DateTimeField(source='created_at')
    isMembership = serializers.BooleanField(source='is_membership')
    remainingNumber = serializers.IntegerField(source='remaining_number')
    expiryDate = serializers.DateField(source='expiry_date')
    latitude = serializers.FloatField(source='point.x')
    longitude = serializers.FloatField(source='point.y')

    class Meta:
        model = Ticket
        fields = ['id', 'location', 'address', 'price', 'mainImage', 'createAt', 'state', 'tags', 'images',
                  'isMembership', 'remainingNumber', 'expiryDate', 'latitude', 'longitude', 'distance', ]
        extra_kwargs = {
            'id': {'help_text': 'Ticket ID'},
        }

    def get_distance(self, ticket, user):
        self.context.user_point
        ticket.point.distance(user.point) * 100 * 1000  # meter 단위로 환산


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
