from django.core.paginator import Paginator, EmptyPage
from .models import Comic, Genre, Chap, Image, Comment, Rating
from .serializers import ComicSerializer, ChapSerializer, CommentSerializer, ComicSerializerBasicInfo, ComicSerializerDetail, ImageSerializer, GenreSerializer, CommenReplytSerializer, CommentPutSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.utils import timezone
from django.db.models import Q, Avg, Max, Sum, F
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from user.serializers import BookMarkSerializer
from user.models import MyUser, BookMark
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


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
        if genreSlug:
            genre = Genre.objects.get(slug=str(genreSlug))
            comicsSofted = comicsSofted.filter(genres=genre)

        paginator = Paginator(comicsSofted, 36)

        # If sort by view count by day, week, month just return 7 comic
        if sort_field == '-view_day' or sort_field == '-view_week' or sort_field == '-view_month' and not genreSlug and not status:
            paginator = Paginator(comicsSofted, 7)

        # If sort by view count just return 20 comic
        if sort_field == '-view' and not genreSlug and not status:
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
    images = Image.objects.filter(chap_id=chap_id).order_by("order")
    serializer = serializer_class(images, many=True)

    response = Response(serializer.data)

    increateView = request.COOKIES.get(str(chap_id))

    try:
        chap = Chap.objects.get(pk=chap_id)

        if not increateView:
            comic = chap.comic
            comic.view += 1
            comic.view_day += 1
            comic.view_week += 1
            comic.view_month += 1
            comic.save()
            response.set_cookie(str(chap_id), str(chap_id), max_age=60 * 5)

        print(increateView)

        return response
    except Chap.DoesNotExist:
        return Response({'error': 'Chap not found'}, status=status.HTTP_404_NOT_FOUND)

# GET - api/comics/genres


@api_view(['GET'])
def getGenres(request):
    serializer_class = GenreSerializer
    genres = Genre.objects.all()
    serializer = serializer_class(genres, many=True)
    return Response(serializer.data)

######## COMMENT ###########

# GET API-CMT  /comics/comic_id

#POST cmt in chap

class MyPagination(PageNumberPagination):
    page_size = 15
@api_view(['POST', 'GET'])
def CommentAPI(request):
    if request.method == 'POST':

        content = request.data.get('content')
        parent_id = request.data.get('parent_id')
        comic_id = request.data.get('comic_id')
        chap_id = request.data.get('chap_id')
        if request.user.is_authenticated:
            user = request.user
            if parent_id == None:
                data = Comment.objects.create(user=user, comic_id=comic_id, chap_id=chap_id, content=content, )
            else:
                parent = Comment.objects.get(id=parent_id)
                data = Comment.objects.create(user=user, comic_id=id, chap_id=chap_id, content=content, parent=parent, )
            data.save()
            serializer_comment = CommentSerializer(data)
            return Response(serializer_comment.data, status=status.HTTP_201_CREATED)
        return Response({'msg': 'user not authenticated'})

    if request.method == 'GET':
        comments = Comment.objects.filter(removed=False, parent=None).order_by('-created_at')
        paginator = MyPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommenReplytSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def get_cmt_comic(request, comic_id):
    if request.method == 'GET':
        print('haha')
        comments = Comment.objects.filter(comic=comic_id, removed=False, parent=None).order_by('-created_at')
        paginator = MyPagination()
        result_page = paginator.paginate_queryset(comments, request)
        serializer = CommenReplytSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


#SORT cmt 1=newest, other=oldest
@api_view(['GET'])
def comment_sort(request, comic_id, record_type=None):
    if record_type == 'newest':
        comments = Comment.objects.filter(comic=comic_id, removed=False, parent=None).order_by('-created_at')

    elif record_type == 'oldest':
        comments = Comment.objects.filter(comic=comic_id, removed=False, parent=None).order_by('-created_at')
    else:
        # handle invalid record_type here
        return Response(status=status.HTTP_400_BAD_REQUEST)
    paginator = MyPagination()
    result_page = paginator.paginate_queryset(comments, request)
    serializer = CommenReplytSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# DELETE and PUT, 1 fields content can update
@api_view(['PUT', 'DELETE'])
def put_comment(request, cmt_id):
    if request.method == 'PUT':
        try:
            cmt = Comment.objects.get(id=cmt_id)
        except Comment.DoesNotExist:
            return Response({'msg': 'this comment not found'}, status=400)
        if request.user.is_authenticated:
            cmt.edited = True
            serializer = CommentPutSerializer(cmt, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({'msg': 'user not authenticated'})

    elif request.method == 'DELETE':
        try:
            cmt = Comment.objects.get(id=cmt_id)
        except Comment.DoesNotExist:
            return Response({'msg': 'this comment not found'}, status=400)
        if request.user.is_authenticated:
            cmt.removed = True
            cmt.save()
            return Response({'msg': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'user not authenticated'})



@api_view(['POST'])
def like_cmt(request, cmt_id):
    if request.method == 'POST':
        cmt = get_object_or_404(Comment, id=cmt_id)
        user = request.user
        if user.is_authenticated:
            if user in cmt.likes.all():
                cmt.likes.remove(user)
                message = 'unliked'
            else:
                cmt.likes.add(user)
                message = 'liked'
            data = {'message': message, 'likes': cmt.likes.count()}
            cmt.likes_num = cmt.likes.count()
            cmt.save()
            return JsonResponse(data)
        else:
            data = {'message': 'User not authenticated'}
            return JsonResponse(data, status=401)


@api_view(['POST'])
def rate_view_API(request, comic_id):
    stars = request.data.get('stars')
    if request.user.is_authenticated:
        user = request.user
        Rating.objects.update_or_create(user=user, comic_id=comic_id, defaults={'stars': stars})
        comics = Comic.objects.get(id=comic_id)
        rates = Rating.objects.filter(comic=comic_id, removed=False).aggregate(Avg('stars'))['stars__avg']
        comics.rating = rates
        comics.save()
        return Response(rates, status=200)
    return Response({'msg': 'user not authenticated'})


# class caculate_recommendations():
#     comics = Comic.objects.filter()
#     total_ratings = Comic.objects.aggregate(total_ratings=Sum('rating'))['total_ratings'] or 1
#     total_views = Comic.objects.aggregate(total_views=Sum('view'))['total_views'] or 1
#     max_update_time = comics.aggregate(max_update_time=Max('updated_at'))['max_update_time'] or timezone.now()
#
#     for i in comics:
#         time_since_update = (timezone.now() - i.updated_at).total_seconds() / (3600 * 24 * 365)
#         weight = (0.5 * F('num_ratings') / total_ratings +
#                   0.3 * F('num_views') / total_views +
#                   0.2 * (1 / (1 + time_since_update)))