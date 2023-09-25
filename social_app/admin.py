from django.contrib import admin
from django.contrib.auth.models import Group

from social_app.models import Post, Comment, Profile, Like

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

admin.site.unregister(Group)
