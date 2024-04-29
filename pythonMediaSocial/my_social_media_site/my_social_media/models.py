from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField



# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:  # xem class BaseModel la lop truu tuong
        abstract = True


class Interaction(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Membership(BaseModel):
    group_name = models.CharField(max_length=200)

    def __str__(self):
        return self.group_name


class User(AbstractUser):
    avatar = CloudinaryField(null=True)
    cover_photo = CloudinaryField(null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    number_phone = models.CharField(max_length=20, null=True, blank=True)

    # many-to-many voi Group
    membership = models.ManyToManyField(Membership, related_name='users', blank=True)
    posts_comments = models.ManyToManyField('Post', through='Comment', related_name='comments_users')
    posts_likes = models.ManyToManyField('Post', through='Like', related_name='likes_users')


# many-to-many user and post
class Comment(Interaction):
    comment = models.TextField()

    def __str__(self):
        return self.comment


class Like(Interaction):
    type_of_like = models.ForeignKey('LikeType', on_delete=models.CASCADE,
                                     related_query_name='Likes')

    class Meta:
        unique_together = [['user', 'post']]  # 1 like với mỗi bài post


class PostType(models.Model):
    name_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name_type


class LikeType(models.Model):
    name_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name_type


class Post(BaseModel):
    title = models.CharField(max_length=100)
    content = RichTextField()
    type_of_post = models.ForeignKey(PostType, on_delete=models.CASCADE,
                                     related_query_name='posts')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_query_name='users')
    membership = models.ManyToManyField(Membership, related_name='membership_posts', blank=True)

    def __str__(self):
        return self.title


# Survey
class Survey(BaseModel):
    title = models.CharField(max_length=100)
    description = RichTextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_query_name='surveys')

    def __str__(self):
        return self.title


class Question(models.Model):
    content = models.TextField(max_length=100)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE,
                               related_query_name='questions')

    def __str__(self):
        return self.content


class Answer(models.Model):
    content = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE,
                                  related_query_name='answers')

    def __str__(self):
        return self.content
# kết thúc phần Survey