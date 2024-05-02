from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics, parsers
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import LikeType, Post, Comment, Like, User
from .serializers import LikeTypeSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserSerializer
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


class PostViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

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


class CommentViewSet(viewsets.ModelViewSet, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeTypeViewSet(viewsets.ModelViewSet):
    queryset = LikeType.objects.all()
    serializer_class = LikeTypeSerializer
