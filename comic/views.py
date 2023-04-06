from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from .models import Comic, Genre, Chap, Comment, Rating, History
from .serializers import ComicSerializer, ChapSerializer, CommentPostSerializer
from .serializers import CommentPutSerializer, ComicHistorySerializer, CommenReplytSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from django.db.models import Avg


def index(request):
    return HttpResponse("comics")


# GET - api/comics/<sort_field>/<page_num>
def getComicBySortFiled(request, page_num, sort_field):
    try:
        comicsSofted = Comic.objects.all().order_by(sort_field)

        #sort by gender:
        if sort_field == '-gender':
            comicsSofted = comicsSofted.filter(gender='female')
        if sort_field == 'gender':
            comicsSofted = comicsSofted.filter('male')


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
    #
    # try:
    #     # Get newest chap
    #     comicsSofted = Comic.objects.all().order_by(sort_field)
    #     paginator = Paginator(comicsSofted, 10)
    #     page_comic = paginator.page(page_num)

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

            latest_chaps = Chap.objects.filter(comic=comic).order_by('-updated_at')[:3]
            serialized_chap = ChapSerializer(instance=latest_chaps, many=True)

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
            "latest_chaps": serialized_chap.data
            # 'sumary': comic.sumary,
            # 'status': comic.status,
            # 'genres': serialized_genres,
            # 'other_name': comic.other_name,
            # 'author': comic.author,
        }
        serialized_comics.append(serialized_comic)

    return JsonResponse(serialized_comics, safe=False)


# GET - api/comics/<comic_id>
@api_view(['GET'])
def getComicDetail(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    if not comic: return JsonResponse({'error': 'Not exist comic'}, status=400)

    serialized_comic = ComicSerializer(instance=comic)

    return Response(serialized_comic.data, status=status.HTTP_200_OK)


######## COMMENT ###########

# GET API-CMT  /comics/comic_id
class CommentAPI(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentPostSerializer

    def get(self, request, id, id_chap):
        comments = Comment.objects.filter(comic=id, removed=False, parent=None).order_by('-created_at')
        serializer_reply = CommenReplytSerializer(comments, many=True)
        return Response(serializer_reply.data, status=200)

    def post(self, request, id, id_chap):
        content = request.data.get('content')
        parent_id = request.data.get('parent_id')
        if request.user.is_authenticated:
            user = request.user
            if parent_id == None:
                data = Comment.objects.create(user=user, comic_id=id, chap_id=id_chap, content=content, )
            else:
                parent = Comment.objects.get(id=parent_id)
                data = Comment.objects.create(user=user, comic_id=id, chap_id=id_chap, content=content, parent=parent, )
            data.save()
            serializer_comment = CommentPostSerializer(data)
            return Response(serializer_comment.data, status=status.HTTP_201_CREATED)
        return Response({'msg': 'user not authenticated'})


# 1 fields content can update
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


@api_view(['GET'])
def like_cmt(request, cmt_id):
    if request.method == 'GET':
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
        try:
            data = Rating.objects.create(user=user, comic_id=comic_id, stars=stars)
        except:
            return Response({'msg': '1 user only rate 1 times'})
        data.save()
        comics = Comic.objects.get(id=comic_id)
        rates = Rating.objects.filter(comic=comic_id, removed=False).aggregate(Avg('stars'))['stars__avg']
        comics.rating = rates
        comics.save()
        return Response(rates, status=200)
    return Response({'msg': 'user not authenticated'})


# HISTORY API
@api_view(['POST'])
def history(request, comic_id, chap_id):
    if request.method == 'POST':
        user = request.user
        if user.is_authenticated:
            try:
                history, created = History.objects.update_or_create(comic_id=comic_id, user=user,
                                                                    defaults={'chap_id': chap_id}, )
                history.save()
                return Response({'msg': 'history add'})
            except:
                return Response({'msg': 'invalid'})
        return Response({'msg': 'user not authenticated'})


@api_view(['GET'])
def history_view(request):
    if request.method == 'GET':
        user = request.user
        history = History.objects.filter(user=user, removed_history=False)
        serializer_history = ComicHistorySerializer(history, many=True)
        return Response(serializer_history.data, status=200)
