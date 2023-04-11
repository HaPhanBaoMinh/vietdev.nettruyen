from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import MyUser, Follow, BookMark
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from comic.serializers import ComicSerializer, ComicSerializerBasicInfo, ChapSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'avatar', 'fullname')

class UserchangeAvatarSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['avatar']

class FollowSerializer(ModelSerializer):
    comic = ComicSerializerBasicInfo()

    class Meta:
        model = Follow
        fields = ('comic', 'readed')
        depth = 1


class FollowSerializerFull(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class BookMarkSerializer(ModelSerializer):
    class Meta:
        model = BookMark
        fields = '__all__'


class BookMarkDetailSerializer(ModelSerializer):
    comic = serializers.SerializerMethodField()
    chap_bookmark = serializers.SerializerMethodField()

    def get_chap_bookmark(self, obj):
        return ChapSerializer(obj.chap).data

    def get_comic(self, obj):
        return ComicSerializerBasicInfo(obj.comic).data

    class Meta:
        model = BookMark
        fields = ('comic', 'chap_bookmark')
        depth = 1
