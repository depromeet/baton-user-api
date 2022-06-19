from django.urls import path
from mypage.views import user_views, ticket_views


urlpatterns = [
    path('users', user_views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>', user_views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:user>/account', user_views.UserAccountView.as_view(), name='user-account'),
    path('users/<int:pk>/address', user_views.UserAddressView.as_view(), name='user-address'),
    path('users/<int:pk>/bookmarks', user_views.UserBookmarkView.as_view(), name='user-bookmark'),  # TODO pk 대신 user
    path('users/<int:pk>/buys', user_views.UserBuyView.as_view(), name='user-buy'),
    path('users/<int:pk>/sells', user_views.UserSellView.as_view(), name='user-sell'),

    path('buys', ticket_views.BuyCreateView.as_view(), name='buy-create'),
    path('buys/<int:pk>', ticket_views.BuyDetailView.as_view(), name='buy-detail'),
    path('bookmarks', ticket_views.BookmarkCreateView.as_view(), name='bookmark-create'),
    path('bookmarks/<int:pk>', ticket_views.BookmarkDetailView.as_view(), name='bookmark-detail'),
]
