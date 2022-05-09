from django.urls import path
from mypage.views import user_views, ticket_views

app_name = 'mypage'


urlpatterns = [
    path('users/<int:pk>', user_views.UserDetailView.as_view(), name='user-detail'),
    path('users/<int:pk>/bookmarks', user_views.UserBookmarkView.as_view(), name='user-bookmark'),
    path('users/<int:pk>/buys', user_views.UserBuyView.as_view(), name='user-buy'),
    path('users/<int:pk>/sells', user_views.UserSellView.as_view(), name='user-sell'),

    path('buys', ticket_views.BuyListView.as_view(), name='buy-list'),
    path('buys/<int:pk>', ticket_views.BuyDetailView.as_view(), name='buy-detail'),
    path('bookmarks', ticket_views.BookmarkListView.as_view(), name='bookmark-list'),
    path('bookmarks/<int:pk>', ticket_views.BookmarkDetailView.as_view(), name='bookmark-detail'),
]
