from django.urls import path, re_path, include
from rest_framework import routers
from my_social_media import views


router = routers.DefaultRouter()
router.register('liketypes', views.LikeTypeViewSet)
router.register('posts', views.PostViewSet)
router.register('users', views.UserViewSet)
router.register('likes', views.LikeViewSet)
router.register('comments', views.CommentViewSet)
router.register('surveys', views.SurveyViewSet)
router.register('questions', views.QuestionViewSet)
router.register('answers', views.AnswerViewSet)


urlpatterns = [
    path('', include(router.urls))
]
