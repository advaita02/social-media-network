from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import LikeType, Post, Comment, Like, User
from .serializers import LikeTypeSerializer, PostSerializer, CommentSerializer, LikeSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    #
    # @action(detail=False, methods=['post'])
    # def create_post(self, request):
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         if not request.user.is_authenticated:
    #             return Response({"message": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    #
    #         serializer.validated_data['created_by'] = request.user
    #         post = serializer.save()
    #         return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeTypeViewSet(viewsets.ModelViewSet):
    queryset = LikeType.objects.all()
    serializer_class = LikeTypeSerializer

