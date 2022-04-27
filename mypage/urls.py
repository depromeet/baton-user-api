from django.urls import path
from mypage.views import BookmarkView, BuyView, SellView

app_name = 'mypage'


urlpatterns = [
    path('<int:pk>/bookmarks', BookmarkView.as_view(), name='bookmark'),
    path('<int:pk>/buys', BuyView.as_view(), name='buy'),
    path('<int:pk>/sells', SellView.as_view(), name='sell'),
]
