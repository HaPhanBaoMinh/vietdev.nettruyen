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

class CommentSerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'comic', 'user', 'content', 'created_at', 'update_at', 'removed', 'edited', 'chap', 'likes_num']


class CommenReplytSerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    user = UserSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comic', 'user', 'content', 'created_at', 'update_at', 'removed', 'edited', 'chap', 'replies', 'likes_num']

    def get_replies(self, obj, depth=0):
        if depth == 1:
            return []
        else:
            replies = Comment.objects.filter(parent=obj.id)
            serializer = CommentSerializer(instance=replies, many=True)
            return serializer.data



class CommentPutSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'content')


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