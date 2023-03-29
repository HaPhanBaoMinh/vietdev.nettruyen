from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('/search', views.getComicSearch),
    path('/genres', views.getGenres),
    path('/chap/image/<int:chap_id>', views.getChapImage),
    path('/<str:genre_slug>', views.getComicByGenreSlug),
    path('/detail/<int:comic_id>', views.getComicDetail),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled),
]
