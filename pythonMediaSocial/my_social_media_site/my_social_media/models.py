from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:  # xem class BaseModel la lop truu tuong
        abstract = True


class Group(BaseModel):
    group_name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(BaseModel):
    name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    number_phone = models.CharField(max_length=20, null=True, blank=True)
    user_role = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    # many-to-many voi Group
    groups = models.ManyToManyField(Group)
    posts_comments = models.ManyToManyField('Post', through='Comment')
    posts_likes = models.ManyToManyField('Post', through='Like')

    def __str__(self):
        return self.name


# many-to-many user and post
class Comment(BaseModel):
    comment = models.TextField()

    def __str__(self):
        return self.name


class Like(BaseModel):
    type_of_like = models.ForeignKey('TypeOfLike', on_delete=models.CASCADE,
                                     related_query_name='Likes')

    def __str__(self):
        return self.name


class TypeOfPost(models.Model):
    name_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TypeOfLike(models.Model):
    name_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    type_of_post = models.ForeignKey(TypeOfPost, on_delete=models.CASCADE,
                                     related_query_name='posts')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_query_name='users')

    def __str__(self):
        return self.name


# Survey
class Survey(BaseModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.name


class Question(models.Model):
    content = models.TextField(max_length=100)
    Survey = models.ForeignKey(Survey, on_delete=models.CASCADE,
                               related_query_name='questions')

    def __str__(self):
        return self.name


class Answer(models.Model):
    content = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    questions = models.ForeignKey(Question, on_delete=models.CASCADE,
                                  related_query_name='answers')

    def __str__(self):
        return self.name
# kết thúc phần Survey
