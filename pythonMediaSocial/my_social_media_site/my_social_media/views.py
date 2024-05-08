from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics, parsers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import LikeType, Post, Comment, Like, User, Membership, PostType
from .serializers import LikeTypeSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserSerializer, \
    PostDetailsSerializer
from .perms import OwnerPermission
from django.shortcuts import get_object_or_404


# from my_social_media import serializers


class UserViewSet(viewsets.ViewSet, generics.ListAPIView,
                  generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    @action(methods=['get'], detail=True)
    def posts(self, request, pk):
        posts = self.get_object().post_set.filter(active=True).all()

        return Response(PostSerializer(posts, many=True,
                                       context={'request': request}).data,
                        status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(UserSerializer(request.user).data)


class PostViewSet(viewsets.ViewSet, generics.ListAPIView,
                  generics.RetrieveAPIView, generics.UpdateAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = PostDetailsSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment']:
            return [permissions.IsAuthenticated]
        return self.permission_classes

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(subject__icontains=q)
        return queries

    @action(detail=True, methods=['post'])
    def create_post(self, request, pk):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            if not request.user.is_authenticated:
                return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            serializer.validated_data['created_by'] = request.user
            post = serializer.save()
            return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, post=self.get_object(),
                                         comment=request.data.get('comment'))
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def add_like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user,
                                                   post=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        like_type_name = request.data.get('like_type_name', None)
        # None ở đây là giá trị mặc định nếu không có kiểu like
        if like_type_name:
            like_type, _ = LikeType.objects.get_or_create(name_type=like_type_name)
            like.type_of_like = like_type
            like.save()

        return Response(PostDetailsSerializer(self.get_object(), context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet, generics.DestroyAPIView,
                     generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OwnerPermission]


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeTypeViewSet(viewsets.ModelViewSet):
    queryset = LikeType.objects.all()
    serializer_class = LikeTypeSerializer


class LikeTypeListAPIView(generics.ListCreateAPIView):
    queryset = LikeType.objects.all()
    serializer_class = LikeTypeSerializer


class LikeTypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
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
