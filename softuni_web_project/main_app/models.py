from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Hashtag(models.Model):
    HASHTAG_MAX_LENGTH = 200
    name = models.CharField(
        max_length=HASHTAG_MAX_LENGTH,
    )


class Post(models.Model):
    CAPTION_MAX_LENGTH = 200
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=CAPTION_MAX_LENGTH,
    )

    photo = models.ImageField(
        null=True,
        blank=True,
        # validators=(
        #     validate_file_max_size(5),
        # )
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.ManyToManyField(
        UserModel,
        related_name='post_likes'
    )

    hashtags = models.ManyToManyField(
        Hashtag,
    )


class Comment(models.Model):
    COMMENT_MAX_LENGTH = 200
    content = models.CharField(
        max_length=COMMENT_MAX_LENGTH,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
