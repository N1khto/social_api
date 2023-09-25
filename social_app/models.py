import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify


def avatar_image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.full_name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads", "avatars", filename)


class Profile(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = "Male"
        FEMALE = "Female"
        OTHER = "Other"

    owner = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField(blank=True)
    gender = models.CharField(
        max_length=63, choices=GenderChoices.choices, null=True
    )
    avatar = models.ImageField(
        null=True, blank=True, upload_to=avatar_image_path
    )
    bio = models.TextField()
    followed = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["-last_name"]


class Post(models.Model):
    header = models.CharField(max_length=255)
    content = models.TextField()
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    created_at = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.header

    class Meta:
        ordering = ["created_at"]


class Comment(models.Model):
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="user_comments",
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    created_at = models.TimeField(auto_now_add=True)
    content = models.CharField(max_length=511)

    class Meta:
        ordering = ["created_at"]


class Like(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="user_likes"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_likes"
    )
