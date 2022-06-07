from mypage.models import User
from mypage.serializers import user_serializers as serializers

from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import Http404
from django.shortcuts import get_object_or_404


class UserCreateView(generics.CreateAPIView):
    """
    사용자 생성 (회원가입)
    """
    serializer_class = serializers.UserCreateSerializer


class UserDetailView(generics.RetrieveDestroyAPIView):
    """
    마이페이지 (+회원탈퇴)
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        마이페이지; 사용자ID가 {id}인 사용자의 상세 정보
        """
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
        ],
    )
    def delete(self, request, *args, **kwargs):
        """
        회원탈퇴; 사용자ID가 {id}인 사용자 삭제
        """
        return self.destroy(request, *args, **kwargs)


class UserSellView(generics.ListAPIView):
    """
    판매내역
    """
    serializer_class = serializers.TicketListSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        state = self.request.query_params.get('state', '0')
        if state not in {'0', '2'}:
            raise Http404('Ticket state value error.')
        return user.sell_tickets.filter(state=state)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
            openapi.Parameter('state', openapi.IN_QUERY, default=0, type=openapi.TYPE_STRING,
                              description='조회할 양도권 상태 (0: 판매중, 2: 판매완료)'),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        판매내역; 사용자ID가 {id}인 사용자가 구매한 양도권 목록
        """
        return super().get(request, *args, **kwargs)


class UserBuyView(generics.ListAPIView):
    """
    구매내역
    """
    serializer_class = serializers.UserBuySerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        return user.buys

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        구매내역; 사용자ID가 {id}인 사용자가 판매한 양도권 목록
        """
        return super().get(request, *args, **kwargs)


class UserBookmarkView(generics.ListAPIView):
    """
    관심상품
    """
    serializer_class = serializers.UserBookmarkSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        state = self.request.query_params.get('state')
        if state:
            if state == '':
                return user.bookmarks.all()
            elif state in {'0', '1', '2'}:
                return user.bookmarks.filter(ticket__state=state)
            else:
                raise Http404('Ticket state value error.')
        return user.bookmarks

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='사용자ID'),
            openapi.Parameter('state', openapi.IN_QUERY, default='', type=openapi.TYPE_STRING,
                              description="조회할 양도권 상태 ((blank): 전체, 0: 판매중, 1: 예약중, 2: 판매완료)"),
        ],
    )
    def get(self, request, *args, **kwargs):
        """
        관심상품; 사용자ID가 {id}인 사용자의 관심상품 목록
        """
        return super().get(request, *args, **kwargs)
