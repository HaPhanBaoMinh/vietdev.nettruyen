from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from user.models import MyUser, Follow
from django.contrib.auth.models import User
from .serializers import UserSerializer, FollowSerializer, FollowSerializerFull, UserchangeAvatarSerializer
from .utils import get_tokens_for_user
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.mail import send_mail
from django.conf import settings
from comic.models import Comic
from django.shortcuts import get_object_or_404

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['id'] = user.id
        # ...
 
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user information to response data
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'avatar': self.user.avatar.url,
            # add other user information fields as needed
        }

        return data
class MyTokenObtainPairView(TokenObtainPairView):
    try:
        serializer_class = MyTokenObtainPairSerializer
    except Exception as e:
        print(e)

@api_view(['POST'])
def sendEmailResetPassword(request):
    email = request.data.get("email")

    if not email:
        return JsonResponse({'error': 'Please enter email'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = MyUser.objects.get(email=email)
        token = get_tokens_for_user(user)
        subject = "RESET PASSWORD NETTRUYEN"
        linkToResetPassword = token["token"]
        message = f'Hi {user.username}, click here to set new password: {linkToResetPassword}  '
        email_from = settings.EMAIL_HOST_USER
        receive_email = [user.email]
        print(message)
        send_mail(subject, message, email_from, receive_email)

        return JsonResponse({"message": "Check your email"})
    except MyUser.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def resetPassword(request):
    token = request.data.get('token')
    resetPassword = request.data.get('password')
    try:
        if not token: return JsonResponse({"message": "Please enter token"}) 
        if not user: return JsonResponse({"message": "Not exist user"}) 
        if not resetPassword: return JsonResponse({"message": "Please enter password"}) 


        payload = jwt.decode(token, "secret", algorithms=['HS256'])
        user_id = payload['user_id']
        user = MyUser.objects.get(pk=user_id)


        user.set_password(resetPassword)
        user.save()
        tokenFormat = RefreshToken(request.data.get('token'), verify=True)
        tokenFormat.blacklist()
      
        return JsonResponse({"message": "Password changed"}, status=status.HTTP_200_OK)
   
    except TokenError as error:
        return JsonResponse({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError as error:
        return JsonResponse({"message": str(error.message)})

# POST - /api/users/register
@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Please provide username, password and email.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create the user object
        user = MyUser.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        return Response({'success': 'User created successfully!'}, status=status.HTTP_201_CREATED)

    except:
        return Response({'error': 'Unable to create user. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST - /api/users/logout
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refreshToken = request.data.get('refresh_token')
        print(refreshToken)
        if not refreshToken: return JsonResponse({"message": "Please enter token"}) 
        tokenFormat = RefreshToken(refreshToken, verify=True)
        tokenFormat.blacklist()

        return JsonResponse({'message': "Logout!"}, status=status.HTTP_204_NO_CONTENT)
    except TokenError as error:
        return JsonResponse({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

# GET/POST - api/comics/follow
@api_view(['GET', 'POST', "DELETE"])
@permission_classes([IsAuthenticated])
def comicFollow(request):
    user = request.user
    # GET follow comic
    if request.method == 'GET':
        follows = user.follow_set.all()
        serializer = FollowSerializer(instance=follows, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # POST create follow
    if request.method == 'POST':
        if not request.data.get("comic_id"): return JsonResponse({'message': "Please enter comic_id"}, status=status.HTTP_400_BAD_REQUEST)
        comic_id = request.data.get("comic_id")
        comic = get_object_or_404(Comic, pk=comic_id)
        follow = Follow.objects.filter(user=user, comic=comic).first()
        # If exist follow in DB just change status
        if follow:
            follow.unfollow = False
            follow.save()
            serializer = FollowSerializer(instance=follow)
            return JsonResponse({"message": "Success!"}, status=status.HTTP_200_OK)

        
        # If not exist
        follow_data = {
            'user': user.id,
            'comic': comic_id
        }
        
        follow_serializer = FollowSerializerFull(data=follow_data)
        if follow_serializer.is_valid():
            follow_serializer.save()
            return JsonResponse({"message": "Success!"}, status=status.HTTP_200_OK)
        return Response(follow_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        if not request.data.get("comic_id"): return JsonResponse({'message': "Please enter comic_id"}, status=status.HTTP_400_BAD_REQUEST)
        comic_id = request.data.get("comic_id")
        comic = get_object_or_404(Comic, pk=comic_id)
        follow = Follow.objects.filter(user=user, comic=comic).first()
        # If exist follow in DB just change status
        if follow:
            follow.unfollow = True
            follow.save()
            serializer = FollowSerializer(instance=follow)
            return JsonResponse({"message": "Success!"}, status=status.HTTP_200_OK)

def index(request):
    return HttpResponse("user")


# @api_view(['PUT'])

class UploadImageTest:
    pass


# class ImageViewSet(generics.ListCreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = UserchangeAvatarSerializer
#     def Put(self, request, *args, **kwargs):
#         user = request.user
#         serializer = UserchangeAvatarSerializer(id=user.id, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'msg':"done"})
#         return Response(serializer.errors, status=400)

@api_view(['PUT'])
def ImageViewSet(request):
    user = request.user
    serializer = UserchangeAvatarSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': "done"})
    return Response(serializer.errors, status=400)