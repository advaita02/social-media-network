from rest_framework.serializers import ModelSerializer
from .models import LikeType, Post, User, Comment, Like


class LikeTypeSerializer(ModelSerializer):
    class Meta:
        model = LikeType
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_of_birth', 'number_phone', 'avatar', 'cover_photo', 'membership']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    # def create(self, validated_data):
    #     return Post.objects.create(**validated_data)
