from django.urls import path
from mypage.views import user_views

app_name = 'mypage'


urlpatterns = [
    path('<int:pk>', user_views.UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/bookmarks', user_views.BookmarkView.as_view(), name='user-bookmark'),
    path('<int:pk>/buys', user_views.BuyView.as_view(), name='user-buy'),
    path('<int:pk>/sells', user_views.SellView.as_view(), name='user-sell'),
]
