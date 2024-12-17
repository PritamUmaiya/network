from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow


def index(request):
    # Display latest post first
    posts = Post.objects.all().order_by("-timestamp")
    return render(request, "network/index.html", {
        "posts": posts
    })

@login_required
def following(request):
    """Posts of users the user follows"""
    user = request.user
    following = user.following.all()
    posts = []
    for follow in following:
        posts += follow.posts.all()
    return render(request, "network/following.html", {
        "posts": posts
    })

@login_required
@require_POST
def new_post(request):
    user = request.user
    content = request.POST["post"]
    post = Post(user=user, content=content)
    post.save()
    return HttpResponseRedirect(reverse("index"))

def profile(request, username):
    user = User.objects.get(username=username)
    followers = [follower.user for follower in Follow.objects.filter(following=user)]
    posts = user.posts.all().order_by("-timestamp")
    return render(request, "network/profile.html", {
        "user": user,
        "followers": followers,
        "posts": posts
    })

@login_required
def follow(request, profile_id):
    user = request.user
    profile = User.objects.get(pk=profile_id)
    
    if not Follow.objects.filter(user=user, following=profile).exists():
        follow = Follow(user=user, following=profile)
        follow.save()
        return JsonResponse({"message": "Followed"})
    else:
        follow = Follow.objects.get(user=user, following=profile)
        follow.delete()
        return JsonResponse({"message": "Unfollowed"})
        
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
