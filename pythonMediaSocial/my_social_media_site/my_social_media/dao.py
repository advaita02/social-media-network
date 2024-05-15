from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Func
from .models import Post, User
from datetime import datetime
from django.db.models import Count


def get_users_by_year():
    # Sử dụng annotate để tính tổng số lượng người dùng theo từng năm
    users_stats = User.objects.annotate(year=ExtractYear('date_joined')).values('year').annotate(count=Count('id')).order_by('year')
    return users_stats


def get_posts_by_year():
    return Post.objects.values(year=ExtractYear('created_date')).annotate(count=Count('id')).order_by('year')


def get_posts_by_month():
    return Post.objects.annotate(
        year=ExtractYear('created_date'),
        month=ExtractMonth('created_date')
    ).values('year', 'month').annotate(
        count=Count('id')
    ).order_by('year', 'month')


class ExtractQuarter(Func):
    function = 'EXTRACT'
    template = '%(function)s(quarter FROM %(expressions)s)'


def get_posts_by_quarter():
    return Post.objects.annotate(year=ExtractYear('created_date'), quarter=ExtractQuarter('created_date')).values(
        'year', 'quarter').annotate(count=Count('id')).order_by('year', 'quarter')
