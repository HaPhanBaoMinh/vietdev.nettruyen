from django.urls import path
from . import views
from django.http import HttpResponse
from .views import CommentAPI, RateViewAPI

urlpatterns = [
    # path('/', views.index),
    path('/search', views.getComicSearch),
    path('/genres', views.getGenres),
    path('/chap/image/<int:chap_id>', views.getChapImage),
    path('/<str:genre_slug>', views.getComicByGenreSlug),
    path('/detail/<int:comic_id>', views.getComicDetail),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled),
    path('/cmt_like/<int:cmt_id>', views.like_cmt),
    path('/rate/<int:comic_id>', RateViewAPI.as_view()),
    path('/put_cmt/<int:cmt_id>', views.PutComment),
    path('/cmt/<int:id>/<int:id_chap>', CommentAPI.as_view()),
]
