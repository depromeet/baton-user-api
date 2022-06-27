from mypage.models import Ticket, Bookmark, Buy, User, Account

from rest_framework import serializers

# from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.db import connection, transaction

from datetime import datetime
from math import sin, cos, radians, degrees, acos


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
    # id = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    id = serializers.IntegerField()
    account = AccountSerializer(required=False)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'nickname', 'phone_number', 'account',
                  'latitude', 'longitude', 'address', 'detailed_address',
                  'check_terms_of_service', 'check_privacy_policy']

    def to_representation(self, instance: User):
        response = super().to_representation(instance)
        response.update({'latitude': instance.point.x, 'longitude': instance.point.y})
        return response

    @transaction.atomic
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
        # with connection.cursor() as cursor:
        #     cursor.execute(f"UPDATE User SET point=ST_GeomFromText('POINT {longitude} {latitude})', 4326) WHERE id=user.id")
        #     cursor.fetchone()
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
                  'latitude', 'longitude', 'address', 'detailed_address', 'image']  # TODO image 추가


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    마이페이지 사용자 정보수정
    """

    class Meta:
        model = User
        fields = ['nickname', 'phone_number', ]  # TODO image 추가


class UserAddressSerializer(serializers.ModelSerializer):
    """
    사용자 주소 수정
    """
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = User
        fields = ['latitude', 'longitude', 'address', 'detailed_address', ]

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = False
        super().__init__(*args, **kwargs)

    def to_representation(self, instance: User):
        response = super().to_representation(instance)
        response.update({'latitude': instance.point.x, 'longitude': instance.point.y})
        return response

    def update(self, instance, validated_data):
        latitude = validated_data.get('latitude', instance.point.x)
        longitude = validated_data.get('longitude', instance.point.y)
        instance.point = Point(longitude, latitude, srid=4326)
        instance.address = validated_data.get('address', instance.address)
        instance.detailed_address = validated_data.get('detailed_address', instance.detailed_address)
        instance.save()
        # with connection.cursor() as cursor:
        #     cursor.execute(f"UPDATE User SET point=ST_GeomFromText('POINT {longitude} {latitude})', 4326) WHERE id=user.id")
        #     cursor.fetchone()
        return instance


class UserImageSerializer(serializers.ModelSerializer):
    """
    이미지 파일 등록/수정/삭제
    """
    image = serializers.ImageField(use_url=True, allow_null=True)

    class Meta:
        model = User
        fields = ['image']


class TicketListSerializer(serializers.ModelSerializer):
    """
    Ticket list 나올 때 한 티켓에 나타나는 정보
    """
    mainImage = serializers.CharField(source='main_image')
    createAt = serializers.DateTimeField(source='created_at')
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='subject')
    state = serializers.SerializerMethodField()  # get_state()가 자동으로 연결됨
    isMembership = serializers.BooleanField(source='is_membership')
    remainingDay = serializers.SerializerMethodField()  # get_remainingDay()가 자동으로 연결됨
    remainingNumber = serializers.IntegerField(source='remaining_number')
    expiryDate = serializers.DateField(source='expiry_date')
    latitude = serializers.FloatField(source='point.x')
    longitude = serializers.FloatField(source='point.y')
    distance = serializers.SerializerMethodField()  # get_distance()가 자동으로 연결됨
    type = serializers.SerializerMethodField()
    bookmarkId = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'location', 'address', 'price', 'mainImage', 'createAt', 'state', 'tags', 'images',
                  'isMembership', 'remainingDay', 'remainingNumber', 'expiryDate', 'latitude', 'longitude', 'distance',
                  'type', 'bookmarkId']
        extra_kwargs = {
            'id': {'help_text': 'Ticket ID'},
        }

    def get_state(self, obj: Ticket):
        translator = {0: 'SALE', 1: 'RESERVED', 2: 'DONE'}
        return translator[obj.state]

    def get_remainingDay(self, obj: Ticket):
        if obj.expiry_date is None:
            return None
        else:
            return (obj.expiry_date - datetime.now().date()).days

    def get_distance(self, obj: Ticket):
        user = self.context['user']

        lat1, lon1 = radians(user.point.x), radians(user.point.y)
        lat2, lon2 = radians(obj.point.y), radians(obj.point.x)
        long_diff = lon1 - lon2

        distance_radian = sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(long_diff)
        distance_meter = degrees(acos(distance_radian)) * 60 * 1.1515 * 1609.344
        return distance_meter

    def get_type(self, obj: Ticket):
        translator = {0: 'HEALTH', 1: 'PT', 2: 'PILATES_YOGA', 3: 'ETC'}
        return translator[obj.type]

    def get_bookmarkId(self, obj: Ticket):
        user = self.context['user']
        try:
            bookmark = Bookmark.objects.get(ticket=obj, user=user)
        except Bookmark.DoesNotExist:
            return None
        else:
            return bookmark.id


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
