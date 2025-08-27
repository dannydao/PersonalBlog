from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.urls import reverse
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm, ProfileForm



def post_list(request):
    q = (request.GET.get("q") or "").strip()
    posts = Post.objects.all().select_related("author")
    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q) |
            Q(author__username__icontains=q)
        )

    return render(request, "posts/post_list.html", {"posts": posts, "q": q, "page_title": "All Posts"})

@login_required
def my_posts(request):
    q = (request.GET.get("q") or "").strip()
    posts = Post.objects.filter(author=request.user).select_related("author")
    if q:
        post = post.filter(
            Q(title__icontains=q) |
            Q(body__icontains=q)
        )
    return render(request, "posts/post_list.html", { "posts":posts, "q": q, "page_title": "My Posts", "tab_title": "My posts"})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # handle new comment in the same view
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/accounts/login/?next=/post/{slug}/")
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post_detail", slug=post.slug)
        
    else:
        form = CommentForm()
    return render(request, "posts/post_detail.html", {"post": post, "form": form})


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", slug=post.slug)
    
    else:
        form = PostForm()
    return render(request, "posts/post_form.html", {"form": form, "title": "New Post"})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponseForbidden("You can only edit your own posts.")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("post_detail", slug=post.slug)

    else:
        form = PostForm(instance=post)
    return render(request, "posts/post_form.html", {"form": form, "title": "Edit Post"})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden("You can only delete your own posts.")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("post_list")
    return render(request, "posts/post_delete.html", {"post": post})

@require_http_methods(["GET", "POST"])
@login_required
def signout(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("post_list")

@require_http_methods(["POST"])
def comment_delete(request, slug, pk):
    comment = get_object_or_404(Comment, pk=pk, post__slug=slug)
    if not (request.user == comment.author or request.user == comment.post.author or request.user.is_superuser):
        return HttpResponseForbidden("You can only delete your own comments or comments on your posts.")
    post_slug = comment.post.slug
    comment.delete()
    messages.success(request, "Comment deleted.")
    return redirect("post_detail", slug=comment.post.slug)

@login_required
@require_http_methods(["POST"])
def comment_edit(request, slug, pk):
    comment = get_object_or_404(Comment, pk=pk, post__slug=slug)
    if request.user != comment.author:
        return HttpResponseForbidden("You can only edit your own comments.")
    body = (request.POST.get("body") or "").strip()
    if not body:
        messages.error(request, "Comment cannot be empty")
    else:
        comment.body = body
        comment.save()
    return redirect("post_detail", slug=comment.post.slug)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_list")
        
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def profile_detail(request, username):
    owner = get_object_or_404(User, username=username)
    profile, _ = Profile.objects.get_or_create(user=owner)
    return render(request, "profile/profile_detail.html", {"owner": owner, "profile": profile})

@login_required
@require_http_methods(["GET", "POST"])
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile_detail", username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profile/profile_form.html", {"form": form})