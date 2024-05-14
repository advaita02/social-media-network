from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status, generics, parsers
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view, authentication_classes
from rest_framework.response import Response
from .models import LikeType, Post, Comment, Like, User, Membership, PostType, Survey, Question, Answer
from .serializers import (LikeTypeSerializer, PostSerializer, CommentSerializer, LikeSerializer,
                          UserSerializer, PostDetailsSerializer, UserProfileSerializer,
                          CommentCreateSerializer, SurveySerializer, QuestionSerializer, AnswerSerializer)
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

    def get_serializer_class(self):
        if self.action == 'create':
            return PostSerializer
        return PostDetailsSerializer

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
        comment = Comment.objects.create(user=request.user,
                                         post=self.get_object(), comment=request.data.get('comment'))
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


class PostCreateAPIView(viewsets.ViewSet, generics.CreateAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = PostSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OwnerPermission]


class LikeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class LikeTypeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = LikeType.objects.all()
    serializer_class = LikeTypeSerializer


class SurveyViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @action(methods=['get'], detail=True)
    def get_question(self, request, pk):
        survey = self.get_object()
        question = survey.question_set.filter().all()

        return Response(QuestionSerializer(question, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ViewSet, generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(methods=['get'], detail=True)
    def get_answer(self, request, pk):
        question = self.get_object()
        answer = question.answer_set.filter().all()

        return Response(AnswerSerializer(answer, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)
