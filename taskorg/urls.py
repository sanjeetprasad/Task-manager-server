# from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from taskorgapi.views import register_user, login_user
from taskorgapi.views import CategoryView, TagsView, TasksView, UserView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'tasks', TasksView, 'task')
router.register(r"tags", TagsView, "tag")
router.register(r'users', UserView, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
