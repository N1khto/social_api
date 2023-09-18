from django.urls import path, include
from rest_framework import routers

from social_app.views import ProfileViewSet, PostViewSet, LikeViewSet


router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("likes", LikeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social_app"
