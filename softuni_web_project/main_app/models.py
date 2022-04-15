from django.db import models
from softuni_web_project.accounts.models import Profile


class Hashtag(models.Model):
    HASHTAG_MAX_LENGTH = 30
    name = models.CharField(
        max_length=HASHTAG_MAX_LENGTH,
        unique=True,
    )

    def __str__(self):
        return self.name


class Post(models.Model):
    CAPTION_MAX_LENGTH = 130
    caption = models.CharField(
        null=True,
        blank=True,
        max_length=CAPTION_MAX_LENGTH,
    )

    photo = models.ImageField()

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )

    likes = models.ManyToManyField(
        Profile,
        related_name='post_likes',
        null=True,
        blank=True,
    )

    hashtags = models.ManyToManyField(
        Hashtag,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.caption
