from rest_framework import serializers

from social_app.models import Profile
from user.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "owner",
            "first_name",
            "last_name",
            "full_name",
            "birth_date",
            "gender",
            "avatar",
            "bio",
            "followed",
            "created_at",
        )


class ProfileListSerializer(ProfileSerializer):
    profile_id = serializers.IntegerField(source="id", read_only=True)
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "profile_id",
            "owner_id",
            "full_name",
            "bio",
            "avatar",
        )


class ProfileDetailSerializer(ProfileSerializer):
    followed = UserSerializer(many=True, read_only=True)
    followers = ProfileListSerializer(many=True, read_only=True, source="owner.followers")

    class Meta:
        model = Profile
        fields = (
            "id",
            "owner",
            "first_name",
            "last_name",
            "full_name",
            "birth_date",
            "gender",
            "avatar",
            "bio",
            "followed",
            "created_at",
            "followers",
        )
