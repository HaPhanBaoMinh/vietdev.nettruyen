from django.core.paginator import Paginator, EmptyPage
from .models import Comic, Genre, Chap, Image
from .serializers import ComicSerializer, ChapSerializer, ComicSerializerBasicInfo, ComicSerializerDetail, ImageSerializer, GenreSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from user.serializers import BookMarkSerializer
from user.models import MyUser, BookMark
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated


def index(request):
    return HttpResponse("comics")

# GET - api/comics/<sort_field>/<page_num>


def getComicBySortFiled(request, page_num, sort_field):

    try:
        # Get newest chap
        comicsSofted = Comic.objects.all().order_by(sort_field)

        # Sort by gender
        if sort_field == '-gender':
            comicsSofted = comicsSofted.filter(gender='female')

        if sort_field == 'gender':
            comicsSofted = comicsSofted.filter(gender='male')

        # If query parameters status is valid
        status = request.GET.get('status', '')
        if status:
            comicsSofted = comicsSofted.filter(status=status)

        # If query parameters genre is valid
        genreSlug = request.GET.get('genre', '')
        genre = Genre.objects.get(slug=str(genreSlug))
        if genre:
            comicsSofted = comicsSofted.filter(genres=genre)

        paginator = Paginator(comicsSofted, 36)

        # If sort by view count by day, week, month just return 7 comic
        if sort_field == '-view_day' or sort_field == '-view_week' or sort_field == '-view_month':
            paginator = Paginator(comicsSofted, 7)

        # If sort by view count just return 20 comic
        if sort_field == '-view':
            paginator = Paginator(comicsSofted, 20)

        page_comic = paginator.page(page_num)

    except FieldError:
        return JsonResponse({'error': 'Page not found'}, status=404)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)

    serialized_comics = []
    for comic in page_comic:
        serialized_genres = []
        for genre in comic.genres.all():
            serialized_genre = {
                'id': genre.id,
                'name': genre.name,
                'slug': genre.slug
            }
            serialized_genres.append(serialized_genre)

        latest_chaps = Chap.objects.filter(
            comic=comic).order_by('-updated_at')[:3]

        serialized_chaps = []
        if latest_chaps:
            serializer = ChapSerializer(instance=latest_chaps, many=True)
            serialized_chaps = serializer.data

        serialized_comic = {
            'id': comic.id,
            'name': comic.name,
            'created_at': comic.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': comic.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'view': comic.view,
            'rating': comic.rating,
            'image': comic.image.url,
            'follower': comic.follower,
            'comment': comic.comment,
            'chap': comic.chap,
            'genres': serialized_genres,
            "latest_chaps": serialized_chaps,
            "view": comic.view,
            # 'sumary': comic.sumary,
            # 'status': comic.status,
            # 'other_name': comic.other_name,
            # 'author': comic.author,
        }
        serialized_comics.append(serialized_comic)

    return JsonResponse(serialized_comics, safe=False)
# GET - api/comics/<comic_id>


@api_view(['GET'])
def getComicDetail(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    if not comic:
        return JsonResponse({'error': 'Not exist comic'}, status=400)

    serialized_comic = ComicSerializerDetail(instance=comic)

    return Response(serialized_comic.data, status=status.HTTP_200_OK)


# GET - api/comics/<search>
@api_view(['GET'])
def getComicSearch(request):
    serializer_class = ComicSerializerBasicInfo
    query = request.GET.get('value', '')
    print(query)
    if not query:
        return JsonResponse({"message": "No value provided"}, status=status.HTTP_400_BAD_REQUEST)
    comics = Comic.objects.filter(Q(name__icontains=query) | Q(
        author__icontains=query) | Q(summary__icontains=query))

    serializer = serializer_class(comics, many=True)
    return Response(serializer.data)


# GET - api/comics/<genre_slug>
@api_view(['GET'])
def getComicByGenreSlug(request, genre_slug):
    comics = Comic.objects.filter(genres__slug=genre_slug)
    serializer = ComicSerializer(comics, many=True)
    return Response(serializer.data)


# GET - api/comics/chap/image/<chap_num>
# Increate the number of view, view_day, view_week, view_month
@api_view(['GET'])
def getChapImage(request, chap_id):
    serializer_class = ImageSerializer
    images = Image.objects.filter(chap_id=chap_id)
    serializer = serializer_class(images, many=True)

    response = Response(serializer.data)

    increateView = request.COOKIES.get(str(chap_id))

    if not increateView:
        chap = Chap.objects.get(pk=chap_id)
        comic = chap.comic
        comic.view += 1
        comic.view_day += 1
        comic.view_week += 1
        comic.view_month += 1
        comic.save()
        response.set_cookie(str(chap_id), str(chap_id), max_age=60 * 5)

    print(increateView)

    return response

# GET - api/comics/genres


@api_view(['GET'])
def getGenres(request):
    serializer_class = GenreSerializer
    genres = Genre.objects.all()
    serializer = serializer_class(genres, many=True)
    return Response(serializer.data)
