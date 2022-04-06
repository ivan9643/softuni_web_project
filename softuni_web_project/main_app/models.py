from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Hashtag(models.Model):
    name = models.CharField(
        max_length=30,
    )


class Post(models.Model):
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=200,
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

    likes = models.IntegerField(
        default=0,
    )

    hashtags = models.ManyToManyField(
        Hashtag,
        null=True,
        blank=True,
    )


class Comment(models.Model):
    content = models.CharField(
        max_length=200,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )
