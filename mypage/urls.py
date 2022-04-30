from django.urls import path
from mypage.views import UserDetailView, SellView, BuyView, BookmarkView

app_name = 'mypage'


urlpatterns = [
    path('<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('<int:pk>/bookmarks', BookmarkView.as_view(), name='user-bookmark'),
    path('<int:pk>/buys', BuyView.as_view(), name='user-buy'),
    path('<int:pk>/sells', SellView.as_view(), name='user-sell'),
]
