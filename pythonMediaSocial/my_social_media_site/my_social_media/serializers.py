from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer
from .models import LikeType, Post, User, Comment, Like


class UserSerializer(ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    def get_avatar_url(self, obj):
        if obj.avatar:
            avatar_url = obj.avatar.url
            return avatar_url
        else:
            return None

    def get_cover_photo_url(self, obj):
        if obj.cover_photo:
            cover_photo_url = obj.cover_photo.url
            return cover_photo_url
        else:
            return None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'number_phone', 'avatar_url',
                  'cover_photo_url']
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


class LikeTypeSerializer(ModelSerializer):
    class Meta:
        model = LikeType
        fields = ['name_type']


class LikeSerializer(ModelSerializer):
    type_of_like = LikeTypeSerializer()

    class Meta:
        model = Like
        fields = ['user', 'type_of_like']


# class UserPostLikeSerializer(ModelSerializer):
#     avatar_url = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'avatar_url']
#
#     def get_avatar_url(self, obj):
#         if obj.avatar:
#             avatar_url = obj.avatar.url
#             return avatar_url
#         else:
#             return None

class UserInPost(ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar_url']

    def get_avatar_url(self, obj):
        if obj.avatar:
            avatar_url = obj.avatar.url
            return avatar_url
        else:
            return None


class UserProfileSerializer(ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    cover_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'avatar_url', 'cover_photo_url']

    def get_avatar_url(self, obj):
        if obj.avatar:
            avatar_url = obj.avatar.url
            return avatar_url
        else:
            return None

    def get_cover_photo_url(self, obj):
        if obj.cover_photo:
            cover_photo_url = obj.cover_photo.url
            return cover_photo_url
        else:
            return None


class PostSerializer(ModelSerializer):
    created_by = UserInPost()
    # posts_likes = LikeSerializer(source='post_likes', many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_by', 'type_of_post']

    def create(self, validated_data):
        return Post.objects.create(**validated_data)


class CommentSerializer(ModelSerializer):  # chỉnh lại chỗ này theo ('id', 'comment', 'user_id')
    user = UserInPost()

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user']


class PostDetailsSerializer(PostSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, post):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return post.like_set.filter(active=True).exists()
        return False

    class Meta:
        model = Post
        fields = PostSerializer.Meta.fields + ['liked']
