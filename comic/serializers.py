from rest_framework.serializers import ModelSerializer
from comic.models import Comic, Genre, Chap, Image, Comment, Rating
from user.models import MyUser
from rest_framework import serializers


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
    genres = GenreSerializer(many=True)

    class Meta:
        model = Comic
        fields = ["image", "name", "newest_chap", "genres"]

    def get_newest_chap(self, obj):
        newest_chaps = obj.chapter.order_by('-created_at')[:3]
        newest_chaps_data = []
        for chap in newest_chaps:
            newest_chaps_data.append({
                'chap_num': chap.chap_num,
                'name': chap.name,
                "created_at": chap.created_at
            })
        return newest_chaps_data


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ChapSerializer(ModelSerializer):
    class Meta:
        model = Chap
        fields = ['updated_at', 'chap_num', 'name', 'id']


class ComicSerializerDetail(ModelSerializer):
    chap = serializers.SerializerMethodField()

    def get_chap(self, obj):
        print(obj.name)
        return ChapSerializer(obj.chapter.all().order_by("-created_at"), many=True).data

    class Meta:
        model = Comic
        fields = '__all__'
        depth = 1


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image', 'order', 'created_at', 'updated_at')

    created_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(
        format='%Y-%m-%d %H:%M:%S', read_only=True)


class CommentPostSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comic', 'content', 'chap', 'user', 'parent')
        # depth = 1


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username']


class GetComicNameSerializer(ModelSerializer):
    class Meta:
        model = Comic
        fields = ['name']


class CommentSerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'comic', 'user', 'content', 'created_at',
                  'update_at', 'removed', 'edited', 'chap', 'likes_num']


class CommenReplytSerializer(ModelSerializer):
    comic = GetComicNameSerializer()
    user = UserSerializer()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comic', 'user', 'content', 'created_at',
                  'update_at', 'removed', 'edited', 'chap', 'replies', 'likes_num']

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


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'user', 'comic', 'stars')
