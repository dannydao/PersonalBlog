from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/new/", views.post_create, name="post_create"),
    path("post/<slug:slug>/comment/<int:pk>/edit/", views.comment_edit, name="comment_edit"),
    path("post/<slug:slug>comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    path("me/", views.my_posts, name="my_posts"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("post/<slug:slug>/delete/", views.post_delete, name="post_delete"),
]