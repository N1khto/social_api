from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from social_app.models import Profile
from social_app.permissions import IsOwnerOrReadOnly
from social_app.serializers import ProfileSerializer, ProfileListSerializer, ProfileDetailSerializer


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
