from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('/search', views.getComicSearch),
    path('/genres', views.getGenres),
    path('/chap/image/<int:chap_id>', views.getChapImage),
    path('/<str:genre_slug>', views.getComicByGenreSlug),
    path('/detail/<int:comic_id>', views.getComicDetail),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled),path('/cmt/<int:comic_id>/<str:record_type>', views.comment_sort),
    path('/cmt/', views.CommentAPI),
    path('/get_cmt/<int:cmt_num>/', views.get_all_cmt),
    path('/get_cmt/<int:comic_id>/<int:cmt_num>/', views.get_cmt_comic),
    path('/cmt/<int:cmt_num>/<str:record_type>/', views.comment_sort),
    path('/cmt_like/<int:cmt_id>/', views.like_cmt),
    path('/rate/<int:comic_id>/', views.rate_view_API),
    path('/put_cmt/<int:cmt_id>/', views.put_comment),
    # path('/recommend/', views.caculate_recommendations),
    path('/author/', views.get_comic_by_author)
]
