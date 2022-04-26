from django.urls import path
from mypage.views import BookmarkView

app_name = 'mypage'


urlpatterns = [
    path('<int:pk>/bookmarks', BookmarkView.as_view(), name='bookmark'),
]
