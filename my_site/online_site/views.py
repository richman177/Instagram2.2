from .serializers import *
from .models import *
from rest_framework import viewsets, generics, status
from .filters import PostFilter, UserProfileFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import PostNumberPagination
from .permissions import CheckComment
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = UserProfileFilter
    search_fields = ['nike_name']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class UserProfileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class FollowListAPIView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer


class FollowDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowDetailSerializer


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PostFilter
    ordering_fields =['created_date']
    pagination_class = PostNumberPagination
    permission_classes = [IsAuthenticated]


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostSerializer


class PostEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class PostLikeListAPIView(generics.ListAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeListSerializer


class PostLikeDetailAPIView(generics.RetrieveAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeDetailSerializer


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [CheckComment]


class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    serializer_class = CommentSerializer


class CommentEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(owner=self.request.user)


class CommentLikeListAPIView(generics.ListAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeListSerializer


class CommentLikeDetailAPIView(generics.RetrieveAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeDetailSerializer


class StoryListAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializer


class StoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryDetailSerializer


class StoryCreateAPIView(generics.CreateAPIView):
    serializer_class = StorySerializer


class StoryEDITAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def get_queryset(self):
        return Story.objects.filter(owner=self.request.user)


class SaveViewSet(viewsets.ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class SaveItemViewSet(viewsets.ModelViewSet):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)
