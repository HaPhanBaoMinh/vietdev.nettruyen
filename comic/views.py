from django.core.paginator import Paginator, EmptyPage
from .models import Comic, Genre, Chap, Image, Comment, Rating
from .serializers import ComicSerializer, ChapSerializer, ComicSerializerBasicInfo, ComicSerializerDetail, ImageSerializer, GenreSerializer, CommentPostSerializer, RatingSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework import status, generics


def index(request):
    return HttpResponse("comics")

# GET - api/comics/<sort_field>/<page_num>


def getComicBySortFiled(request, page_num, sort_field):

    try:
        # Get newest chap
        comicsSofted = Comic.objects.all().order_by(sort_field)
        paginator = Paginator(comicsSofted, 10)
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
            # 'summary': comic.summary,
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
@api_view(['GET'])
def getChapImage(request, chap_id):
    serializer_class = ImageSerializer
    images = Image.objects.filter(chap_id=chap_id)
    serializer = serializer_class(images, many=True)

    # Add to bookmark (history) if usser login
    user = request.user

    return Response(serializer.data)

# GET - api/comics/genres


@api_view(['GET'])
def getGenres(request):
    serializer_class = GenreSerializer
    genres = Genre.objects.all()
    serializer = serializer_class(genres, many=True)
    return Response(serializer.data)


# GET API-CMT  /comics/comic_id
class CommentAPI(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentPostSerializer

    def get(self, request, id, id_chap):
        comments = Comment.objects.filter(
            comic=id, removed=False, parent=None).order_by('-created_at')
        serializer_reply = CommenReplytSerializer(comments, many=True)
        return Response(serializer_reply.data, status=200)

    def post(self, request, id, id_chap):
        content = request.data.get('content')
        parent_id = request.data.get('parent_id')
        if request.user.is_authenticated:
            user = request.user
            if parent_id == None:
                data = Comment.objects.create(
                    user=user, comic_id=id, chap_id=id_chap, content=content,)
            else:
                parent = Comment.objects.get(id=parent_id)
                data = Comment.objects.create(
                    user=user, comic_id=id, chap_id=id_chap, content=content, parent=parent,)
            data.save()
            serializer_comment = CommentPostSerializer(data)
            return Response(serializer_comment.data, status=status.HTTP_201_CREATED)
        return Response({'msg': 'user not authenticated'})

# 1 fields content can update


@api_view(['PUT', 'DELETE'])
def PutComment(request, cmt_id):
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


class RateViewAPI(generics.ListCreateAPIView):
    queryset = Rating.objects.filter(removed=False).order_by('-created_at')
    serializer_class = RatingSerializer

    def post(self, request, comic_id):
        stars = request.data.get('stars')
        if request.user.is_authenticated:
            user = request.user
            try:
                data = Rating.objects.create(
                    user=user,
                    comic_id=comic_id,
                    stars=stars,
                )
            except:
                return Response({'msg': '1 user only rate 1 times'})
            data.save()
            comics = Comic.objects.get(id=comic_id)
            rates = Rating.objects.filter(comic=comic_id, removed=False).aggregate(
                Avg('stars'))['stars__avg']
            comics.rating = rates
            comics.save()
            return Response(rates, status=200)
        return Response({'msg': 'user not authenticated'})
