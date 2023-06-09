from .views import MyTokenObtainPairView
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password', views.sendEmailResetPassword, name='token_refresh'),
    path('create_new_password', views.resetPassword),
    path('register', views.create_user),
    path('follow', views.comicFollow),
    path('logout', views.logout),
    path('bookmark', views.bookmark),
    path('/', views.index),
    path('upload/', views.ImageViewSet, name='upload'),
    path('follow_anonymous', views.follow_without_login),
    path('follow_sync', views.follow_comic_sync),
]
