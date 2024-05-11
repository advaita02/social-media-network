from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status, generics, parsers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view, authentication_classes
from rest_framework.response import Response
from .models import LikeType, Post, Comment, Like, User, Membership, PostType
from .serializers import (LikeTypeSerializer, PostSerializer, CommentSerializer, LikeSerializer,
                          UserSerializer, PostDetailsSerializer, UserProfileSerializer, CommentCreateSerializer)
from .perms import OwnerPermission
from django.shortcuts import get_object_or_404


# from my_social_media import serializers
class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(detail=True)
    #  xem profile user
    def profile(self, request, pk=None):
        user = self.get_object()
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def posts(self, request, pk):
        user = self.get_object()
        posts = user.post_set.filter(active=True).all()

        return Response(PostDetailsSerializer(posts, many=True,
                                              context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)


class PostViewSet(viewsets.ViewSet, generics.ListAPIView,
                  generics.RetrieveAPIView, generics.UpdateAPIView, generics.CreateAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = PostDetailsSerializer

    def get_permissions(self):
        if self.action in ['add_comment', 'liked', 'create_post']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(subject__icontains=q)
        return queries

    @action(methods=['get'], detail=True)
    def comments(self, request, pk):
        post = self.get_object()
        comment = post.comment_set.filter(active=True).all()

        return Response(CommentSerializer(comment, many=True,
                                          context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add_comment')
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, post=self.get_object(), comment=request.data.get('comment'))
        comment.save()
        return Response(CommentSerializer(comment, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def add_like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user,
                                                   post=self.get_object())
        if not created:
            like.active = not like.active
            like_type_name = request.data.get('like_type_name', None)
            # None ở đây là giá trị mặc định nếu không có kiểu like
            if like_type_name:
                like_type, _ = LikeType.objects.get_or_create(name_type=like_type_name)
                like.type_of_like = like_type
            like.save()

        return Response(PostDetailsSerializer(self.get_object(), context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class PostCreateAPIView(viewsets.ViewSet):
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OwnerPermission]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeTypeViewSet(viewsets.ModelViewSet):
    queryset = LikeType.objects.all()
    serializer_class = LikeTypeSerializer


# membership1 = Membership.objects.create(group_name='default')
# membership2 = Membership.objects.create(group_name='Cuu sinh vien 2020')
#
# post_type1 = PostType.objects.create(name_type='Bao cao')
# post_type2 = PostType.objects.create(name_type='default')
#
# like_type1 = LikeType.objects.create(name_type='like')
# like_type2 = LikeType.objects.create(name_type='love')
# #
# user1 = User.objects.create(username='userNam', email='userNam@gmail.com')
# user1.set_password('123456')
# user1.save()
#
# user2 = User.objects.create(username='userTuan', email='userTuan@gmail.com')
# user2.set_password('123456')
# user2.save()
#
# post1 = Post.objects.create(
#     title='Python da loi thoi',
#     content='Vi no qua don gian va phuc tap',
#     type_of_post=post_type1,
#     created_by=user1
# )
#
# post2 = Post.objects.create(
#     title='Python la ngon ngu tuong lai the gioi',
#     content='Vi la ngon ngu tuong lai nen can tao clb bat tran.',
#     type_of_post=post_type2,
#     created_by=user2
# )
#
# post1.membership.add(membership1)
# post1.membership.add(membership2)
# post2.membership.add(membership1)
#
# like = Like.objects.create(
#     user=user1,
#     post=post1,
#     type_of_like=like_type1
# )
