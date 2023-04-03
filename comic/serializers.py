from rest_framework.serializers import ModelSerializer
from comic.models import Comic, Genre, Chap, Comment, Rating, History
from rest_framework import serializers
from user.models import MyUser
class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        
class ComicSerializer(ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Comic
        fields = '__all__'

class ComicSerializerBasicInfo(ModelSerializer):
    newest_chap = serializers.SerializerMethodField()
    class Meta:
        model = Comic
        fields = ["image", "name", "newest_chap"]

    def get_newest_chap(self, obj):
        newest_chap = obj.chapter.order_by('-created_at').first()
        if newest_chap:
            return {
                'name': newest_chap.name,
                'created_at': newest_chap.created_at,
            }
        return None      

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ChapSerializer(ModelSerializer):
    class Meta:
        model = Chap
        fields = ['updated_at', 'chap_num', 'name']


class GetComicNameSerializer(ModelSerializer):
    class Meta:
        model = Comic
        fields = ['name']

class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username']


class CommentPostSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comic', 'content', 'chap', 'user', 'parent')
        # depth = 1


class CommenReplytSerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'comic', 'user', 'content', 'created_at', 'update_at', 'removed', 'edited', 'chap', 'parent', 'likes_num']
    def to_representation(self, instance):
        res = super(CommenReplytSerializer, self).to_representation(instance)
        return {res['parent']: res}

class CommentSerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'



class CommentPutSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content')


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'comic', 'stars')

class GetChapnum(ModelSerializer):
    class Meta:
        model = Chap
        fields = ['chap_num']
class ComicHistorySerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    chap = GetChapnum()
    class Meta:
        model = History
        fields = ('id', 'comic', 'chap')