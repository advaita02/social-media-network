from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Like, Comment, Membership, Survey, Question, Answer, PostType, LikeType

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'date_joined', 'is_staff')
    search_fields = ('username', 'email')
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','email', 'date_of_birth', 'number_phone', 'avatar', 'cover_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Membership', {'fields': ('membership',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar', 'cover_photo'),
        }),
    )

# Đăng ký CustomUserAdmin với trang admin của Django
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Membership)
admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(PostType)
admin.site.register(LikeType)
