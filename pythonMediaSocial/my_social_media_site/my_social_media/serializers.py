from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import LikeType, Post, User, Comment, Like


class LikeTypeSerializer(ModelSerializer):
    class Meta:
        model = LikeType
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'number_phone', 'avatar',
                  'cover_photo']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class CommentSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user']


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class PostDetailsSerializer(PostSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, request, post):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return post.like_set.filter(active=True).exist()
