from django.db.models import Q, Count
from django.shortcuts import redirect
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from social_app.models import Profile, Post, Like
from social_app.permissions import IsOwnerOrReadOnly
from social_app.serializers import (
    ProfileSerializer,
    ProfileListSerializer,
    ProfileDetailSerializer,
    PostSerializer,
    PostDetailSerializer,
    PostListSerializer,
    LikeSerializer,
)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.select_related("owner").prefetch_related(
        "owner__user_likes__post", "followed__owner", "followers__owner"
    )
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        if self.action == "my_page":
            return ProfileDetailSerializer
        return ProfileSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        bio = self.request.query_params.get("bio")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(
                Q(first_name__icontains=name) | Q(last_name__icontains=name)
            )
        if bio:
            queryset = queryset.filter(bio__icontains=bio)
        return queryset.distinct()

    @action(
        detail=False,
        methods=["get"],
    )
    def my_page(self, request, pk=None):
        """action used retrieve current user's profile"""
        return redirect(
            f"/api/social_app/profiles/{str(self.request.user.profile.pk)}"
        )

    @action(detail=True, methods=["get"])
    def follow(self, request, pk=None):
        """action used to follow or unfollow user profile"""
        profile = get_object_or_404(Profile, owner_id=self.request.user.pk)
        if profile:
            serializer = ProfileSerializer(profile, many=False)
            if int(pk) not in serializer.data.get("followed"):
                profile.followed.add(pk)
            else:
                profile.followed.remove(pk)
            profile.save()
            return redirect(f"/api/social_app/profiles/{pk}")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Search by first or last name (ex. ?name=peter)",
            ),
            OpenApiParameter(
                "bio",
                type=OpenApiTypes.STR,
                description="Search by bio (ex. ?bio=teacher)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.annotate(
        num_likes=Count("post_likes"), num_comments=Count("post_comments")
    )
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        content = self.request.query_params.get("content")
        user = self.request.query_params.get("user")
        queryset = self.queryset
        if content:
            queryset = queryset.filter(
                Q(header__icontains=content) | Q(content__icontains=content)
            )
        if user:
            queryset = queryset.filter(owner_id=user)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "content",
                type=OpenApiTypes.STR,
                description="Search by post content (ex. ?content=pineapples)",
            ),
            OpenApiParameter(
                "user",
                type=OpenApiTypes.STR,
                description="Search by user id (ex. ?user=6)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post, pk=self.request.data["post"])
        if self.request.data.get("like"):
            already_liked = Like.objects.filter(
                post=post_instance, owner=self.request.user
            ).exists()
            if already_liked:
                raise ValidationError(
                    {"message": "You have already liked this post"}
                )
            else:
                serializer.save(post=post_instance, owner=self.request.user)
        elif self.request.data.get("unlike"):
            Like.objects.filter(
                post=post_instance, owner=self.request.user
            ).delete()
