from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from social_app.models import Profile, Post
from social_app.permissions import IsOwnerOrReadOnly
from social_app.serializers import ProfileSerializer, ProfileListSerializer, ProfileDetailSerializer, PostSerializer, \
    PostDetailSerializer, PostListSerializer


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
