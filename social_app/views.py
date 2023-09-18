from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from social_app.models import Profile, Post, Like
from social_app.permissions import IsOwnerOrReadOnly
from social_app.serializers import ProfileSerializer, ProfileListSerializer, ProfileDetailSerializer, PostSerializer, \
    PostDetailSerializer, PostListSerializer, LikeSerializer


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")
        bio = self.request.query_params.get("bio")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if bio:
            queryset = queryset.filter(bio__icontains=bio)
        return queryset.distinct()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,
                          IsOwnerOrReadOnly)

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
        queryset = self.queryset
        if content:
            queryset = queryset.filter(Q(header__icontains=content) | Q(content__icontains=content))
        return queryset.distinct()


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        post_instance = get_object_or_404(Post, pk=self.request.data["post"])
        if self.request.data.get("like"):
            already_liked = Like.objects.filter(post=post_instance, owner=self.request.user).exists()
            if already_liked:
                raise ValidationError({"message": "You have already liked this post"})
            else:
                serializer.save(post=post_instance, owner=self.request.user)
        elif self.request.data.get("unlike"):
            Like.objects.filter(post=post_instance, owner=self.request.user).delete()
