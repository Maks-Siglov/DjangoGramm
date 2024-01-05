from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from my_auth.models import User
from post.forms import CommentForm, PostForm
from post.models import Comment, Image, Post, Tag


@login_required(login_url="login")
def create_post(request) -> HttpResponse:
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()

            if form.cleaned_data["image"]:
                image = request.FILES["image"]
                Image.objects.create(image=image, post=post)

            tag_names = form.cleaned_data["tags"].split(",")
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            return redirect("post_list")
    else:
        form = PostForm()

    return render(request, "post/create_post.html", {"form": form})


def post_list(request) -> HttpResponse:
    posts = Post.objects.all()
    return render(request, "post/post_list.html", {"posts": posts})


def user_posts(request, username: str) -> HttpResponse:
    user = User.objects.get(username=username)
    posts = Post.objects.filter(owner=user)
    if request.user == user:
        return render(request, "post/user_posts.html", {"posts": posts})

    return render(request, "post/post_list.html", {"posts": posts})


@login_required(login_url="login")
def post_detail(request, post_id: int) -> HttpResponse:
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.owner = request.user
            comment.save()

    return render(
        request,
        "post/post_detail.html",
        {"post": post, "comments": comments, "comment_form": comment_form},
    )


@login_required(login_url="login")
def edit_post(request, post_id: int) -> HttpResponseRedirect:
    post = Post.objects.get(id=post_id)
    if request.user != post.owner:
        messages.error(
            request, "You do not have permission to view this userprofile."
        )
        return redirect("post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            tag_names = form.cleaned_data["tags"].split(",")
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("user_posts", post.owner.username)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "post/edit_post.html",
        {"form": form},
    )


@login_required(login_url="login")
def delete_post(request, post_id: int) -> HttpResponse | HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.owner:
        messages.error(
            request, "You do not have permission to view this userprofile."
        )
        return redirect("post_list")

    if request.method == "POST":
        post.delete()
        return redirect("user_posts", post.owner.username)

    return render(
        request,
        "post/delete_post.html",
        {"post": post, "user": post.owner},
    )


@login_required(login_url="login")
def like_post(request, post_id: int) -> HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)

        if user in post.dislikes.all():
            post.dislikes.remove(user)

    return redirect("post_list")


@login_required(login_url="login")
def dislike_post(request, post_id: int) -> HttpResponseRedirect:
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        post.dislikes.add(user)

        if user in post.likes.all():
            post.likes.remove(user)

    return redirect("post_list")


@login_required(login_url="login")
def like_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
    else:
        comment.likes.add(user)

        if user in comment.dislikes.all():
            comment.dislikes.remove(user)

    return redirect("post_detail", comment.post.id)


@login_required(login_url="login")
def dislike_comment(request, comment_id: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)
    else:
        comment.dislikes.add(user)

        if user in comment.likes.all():
            comment.likes.remove(user)

    return redirect("post_detail", comment.post.id)