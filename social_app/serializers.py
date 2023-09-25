from rest_framework import serializers

from social_app.models import Profile, Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "content", "owner", "created_at")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "header", "content", "owner", "created_at")


class PostListSerializer(PostSerializer):
    num_likes = serializers.IntegerField(read_only=True)
    num_comments = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "header",
            "content",
            "owner",
            "num_likes",
            "num_comments",
            "created_at",
        )


class PostDetailSerializer(PostSerializer):
    comments = CommentSerializer(many=True, source="post_comments")
    num_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "header",
            "content",
            "owner",
            "created_at",
            "num_likes",
            "comments",
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "post", "owner")
        read_only_fields = ("id", "owner")


class LikeDetailSerializer(LikeSerializer):
    post = PostSerializer(many=False, read_only=True)

    class Meta:
        model = Like
        fields = ("id", "post", "owner")


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
    followed = ProfileListSerializer(many=True, read_only=True)
    followers = ProfileListSerializer(many=True, read_only=True)
    user_likes = LikeDetailSerializer(many=True, source="owner.user_likes")

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
            "user_likes",
        )
