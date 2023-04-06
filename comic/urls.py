from django.urls import path
from . import views
from django.http import HttpResponse
from .views import CommentAPI

urlpatterns = [
    path('/', views.index),
    path('/<int:comic_id>', views.getComicDetail),
    # path('/cmt/<int:comic_id>', views.GetComment),
    path('/cmt/<int:id>/<int:id_chap>', CommentAPI.as_view()),
    path('/history/<int:comic_id>/<int:chap_id>', views.history),
    path('/history/', views.history_view),
    path('/cmt_like/<int:cmt_id>', views.like_cmt),
    path('/rate/<int:comic_id>', views.rate_view_API),
    path('/put_cmt/<int:cmt_id>', views.put_comment),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled)
]