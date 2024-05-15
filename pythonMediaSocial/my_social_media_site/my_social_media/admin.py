from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.urls import path
from .models import User, Post, Like, Comment, Membership, Survey, Question, Answer, PostType, LikeType
from .dao import get_posts_by_year, get_users_by_year, get_posts_by_month
from django.template.response import TemplateResponse
import json
from .forms import YearForm

# from adminplus.sites import register_view


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'date_joined', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info',
         {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'number_phone', 'avatar', 'cover_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Membership', {'fields': ('membership',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'membership', 'avatar', 'cover_photo'),
        }),
    )


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Post
        fields = '__all__'


class SocialMediaAppAdminSite(admin.AdminSite):
    site_header = "ADMIN SOCIAL MEDIA FOR FORMER STUDENT"

    def get_urls(self):
        return [
            path('posts-by-year-stats/', self.admin_view(self.posts_by_year_stats_view)),
            path('users-by-year-stats/', self.admin_view(self.users_by_year_stats_view)),
            path('posts-by-month-stats/', self.admin_view(self.posts_by_month_stats_view))
        ] + super().get_urls()

    def posts_by_year_stats_view(self, request):
        posts_by_year_stats = get_posts_by_year()

        return TemplateResponse(request, 'admin/stats_posts_by_year_view.html', {
            'posts_by_year_stats': posts_by_year_stats
        })

    def users_by_year_stats_view(self, request):
        users_by_year_stats = get_users_by_year()

        return TemplateResponse(request, 'admin/stats_users_each_year_view.html', {
            'users_by_year_stats': users_by_year_stats
        })

    def posts_by_month_stats_view(self, request):
        year_form = YearForm(request.GET or None)  # Hiển thị form cho người dùng

        if request.method == 'GET' and year_form.is_valid():
            # Lấy năm được chọn từ form
            selected_year = year_form.cleaned_data['year']
            # Thống kê số lượng bài đăng theo tháng cho năm được chọn
            posts_by_month = get_posts_by_month(year=selected_year)
        else:
            # Nếu không có năm nào được chọn, mặc định hiển thị cho năm hiện tại
            posts_by_month = get_posts_by_month()

        # Chuyển đổi dữ liệu sang định dạng JSON
        posts_by_month_json = json.dumps(list(posts_by_month))

        return TemplateResponse(request, 'admin/stats_posts_by_month_view.html', {
            'year_form': year_form,
            'posts_by_month_json': posts_by_month_json
        })


class PostAdmin(admin.ModelAdmin):
    form = PostForm
    list_display = ('title', 'type_of_post', 'created_by', 'created_date', 'updated_date', 'active', 'is_comment')
    search_fields = ('title', 'content', 'created_by__username')
    list_filter = ('type_of_post', 'created_date', 'updated_date', 'active')
    readonly_fields = ('created_date', 'updated_date')
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'type_of_post', 'created_by', 'active', 'is_comment', 'membership')
        }),
        ('Timestamps', {
            'fields': ('created_date', 'updated_date')
        }),
    )
    filter_horizontal = ('membership',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('created_by', 'type_of_post').prefetch_related('membership')


# Custom admin classes
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'type_of_like', 'active')
    search_fields = ('user__username', 'post__title')
    list_filter = ('active', 'type_of_like')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment', 'created_date')
    search_fields = ('user__username', 'post__title', 'comment')
    list_filter = ('created_date',)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'created_date', 'updated_date', 'active')
    search_fields = ('group_name',)
    list_filter = ('active',)


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_date', 'updated_date', 'active')
    search_fields = ('title', 'created_by__username')
    list_filter = ('active', 'created_date')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'survey')
    search_fields = ('content', 'survey__title')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('content', 'questions', 'quantity')
    search_fields = ('content', 'questions__content')


class PostTypeAdmin(admin.ModelAdmin):
    list_display = ('name_type',)
    search_fields = ('name_type',)


class LikeTypeAdmin(admin.ModelAdmin):
    list_display = ('name_type',)
    search_fields = ('name_type',)


# register_view('posts-by-year-stats/', SocialMediaAppAdminSite.as_view(), view=posts_by_year_stats_view)


social_media_admin_site = SocialMediaAppAdminSite(name='social_media_admin')


social_media_admin_site.register(User, CustomUserAdmin)
social_media_admin_site.register(Post, PostAdmin)
social_media_admin_site.register(Like, LikeAdmin)
social_media_admin_site.register(Comment, CommentAdmin)
social_media_admin_site.register(Membership, MembershipAdmin)
social_media_admin_site.register(Survey, SurveyAdmin)
social_media_admin_site.register(Question, QuestionAdmin)
social_media_admin_site.register(Answer, AnswerAdmin)
social_media_admin_site.register(PostType, PostTypeAdmin)
social_media_admin_site.register(LikeType, LikeTypeAdmin)

# Optionally unregister models from the default admin site
# admin.site.unregister(User)
# admin.site.unregister(Post)
# admin.site.unregister(Like)
# admin.site.unregister(Comment)
# admin.site.unregister(Membership)
# admin.site.unregister(Survey)
# admin.site.unregister(Question)
# admin.site.unregister(Answer)
# admin.site.unregister(PostType)
# admin.site.unregister(LikeType)
