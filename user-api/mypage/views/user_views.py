from mypage.models import User, Account
from mypage.serializers import user_serializers as serializers

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404


class UserCreateView(generics.CreateAPIView):
    """
    사용자 생성 (회원가입)
    """
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    마이페이지 (+회원탈퇴)
    """
    queryset = User.objects.all()
    # permission_classes = [permissions.AllowAny]  # TODO Temp

    def get_serializer_class(self):
        if self.request.method in ('GET', 'DELETE'):
            return serializers.UserDetailSerializer
        elif self.request.method in ('PUT', 'PATCH'):
            return serializers.UserUpdateSerializer

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'), ],
    )
    def get(self, request, *args, **kwargs):
        """
        마이페이지; 사용자ID가 {id}인 사용자의 상세 정보
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'), ],
    )
    def delete(self, request, *args, **kwargs):
        """
        회원탈퇴; 사용자ID가 {id}인 사용자 삭제
        """
        return self.destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'), ],
    )
    def patch(self, request, *args, **kwargs):
        """
        정보수정; 사용자ID가 {id}인 사용자의 정보 수정
        """
        return self.partial_update(request, *args, **kwargs)


class UserAccountView(generics.RetrieveUpdateAPIView, generics.CreateAPIView):
    """
    마이페이지 계좌 설정
    """
    queryset = Account.objects.all()
    serializer_class = serializers.AccountSerializer
    lookup_field = 'user'

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('user')
        self.user = get_object_or_404(User, pk=pk)
        if self.user.account is not None:
            return Response({'detail': '이미 계좌가 존재하는 사용자입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return self.create(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):
        self.user.account = serializer.save()
        self.user.save()


class UserAddressView(generics.RetrieveUpdateAPIView):
    """
    사용자 주소 수정
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserAddressSerializer


class UserSellView(generics.ListAPIView):
    """
    판매내역
    """
    serializer_class = serializers.TicketListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.user = get_object_or_404(User, pk=pk)
        state = self.request.query_params.get('state', '0')
        if state not in {'0', '2'}:
            raise Http404('Ticket state value error.')
        elif state == '0':
            state += '1'
        return self.user.sell_tickets.filter(state__in=state)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.user
        return context

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
            openapi.Parameter('state', openapi.IN_QUERY, default=0, type=openapi.TYPE_STRING,
                              description='조회할 양도권 상태 (0: 판매중, 2: 판매완료)'),
        ],
        responses={200: serializers.TicketListSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        판매내역; 사용자ID가 {id}인 사용자가 판매한 양도권 목록
        """
        return self.list(request, *args, **kwargs)


class UserBuyView(generics.ListAPIView):
    """
    구매내역
    """
    serializer_class = serializers.UserBuySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.user = get_object_or_404(User, pk=pk)
        return self.user.buys

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.user
        return context

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'), ],
        responses={200: serializers.UserBuySerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        구매내역; 사용자ID가 {id}인 사용자가 구매한 양도권 목록
        """
        return self.list(request, *args, **kwargs)


class UserBookmarkView(generics.ListAPIView):
    """
    관심상품
    """
    serializer_class = serializers.UserBookmarkSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.user = get_object_or_404(User, pk=pk)
        state = self.request.query_params.get('state')
        if state:
            if state == '':
                return self.user.bookmarks.all()
            elif state in {'0', '1', '2'}:
                return self.user.bookmarks.filter(ticket__state=state)
            else:
                raise Http404('Ticket state value error.')
        return self.user.bookmarks

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.user
        return context

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
            openapi.Parameter('state', openapi.IN_QUERY, default='', type=openapi.TYPE_STRING,
                              description="조회할 양도권 상태 ((blank): 전체, 0: 판매중, 1: 예약중, 2: 판매완료)"),
        ],
        responses={200: serializers.UserBookmarkSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        """
        관심상품; 사용자ID가 {id}인 사용자의 관심상품 목록
        """
        return self.list(request, *args, **kwargs)
