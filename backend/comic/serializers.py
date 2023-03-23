from rest_framework.serializers import ModelSerializer
from comic.models import Comic, Genre, Chap, Image
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
        fields = ['updated_at', 'chap_num', 'name']


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
