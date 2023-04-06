from django.urls import path
from . import views
from django.http import HttpResponse
from .views import CommentAPI

urlpatterns = [
    path('/', views.index),
    path('/<int:comic_id>', views.getComicDetail),
    path('/cmt/<int:id>/<int:id_chap>', views.CommentAPI),
    path('/cmt/<int:comic_id>', views.comment_post_comic_api),
    path('/get_cmt/<int:comic_id>/<int:cmt_num>', views.get_cmt_num),
    path('/cmt/<int:comic_id>/<int:cmt_num>/<int:new>', views.comment_sort),
    path('/cmt_like/<int:cmt_id>', views.like_cmt),
    path('/rate/<int:comic_id>', views.rate_view_API),
    path('/put_cmt/<int:cmt_id>', views.put_comment),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled)
]