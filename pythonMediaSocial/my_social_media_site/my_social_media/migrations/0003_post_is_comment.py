# Generated by Django 5.0.4 on 2024-05-11 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_social_media', '0002_alter_user_avatar_alter_user_cover_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_comment',
            field=models.BooleanField(default=True),
        ),
    ]