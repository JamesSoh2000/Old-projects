from django import http
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import constraints
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
import json

from .utilities import get_next_url, get_previous_url
from .models import User, Post
from .forms import NewPostForm
from django.shortcuts import redirect

def index(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)


    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "page": page,
        "previous_url": get_previous_url(page),
        "next_url": get_next_url(page),
    })

@csrf_exempt
@login_required
def editpost(request, post_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required!'}, status = 400)

    try:
        post = Post.objects.get(pk = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.user == post.author:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']

        Post.objects.filter(pk=post_id).update(content=f'{content}')

        return JsonResponse({"message": "Post updated successfully.", "content": content}, status=200)

    else:
        return JsonResponse({'error': 'You cant'}, status=400)


@csrf_exempt
@login_required
def updatelike(request, post_id):

    user = request.user

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if (user.likes.filter(pk=post_id).exists()):
        post.liked_by.remove(user)
        likes_post = False
    else:
        post.liked_by.add(user)
        likes_post = True

    likes = post.likes()

    return JsonResponse({"likesPost": likes_post, "likesCount": likes}, status=200)


@login_required
def newpost(request):

    if request.method != POST:
        return JsonResponse({"error": "POST request required."}, status=400)

    form = NewPostForm(request.POST)

    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect("index")

def profile(request, user_id):

    profile_user = User.objects.get(pk=user_id)

    posts = Post.objects.filter(author=user_id)
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    if request.user.is_authenticated:
        following = profile_user.followers.filter(pk=request.user.id).exists()
    else:
        following = False

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "following": following,
        "following_count": profile_user.following.all().count(),
        "followers_count": profile_user.followers.all().count(),
        "page": page,
        "previous_url": get_previous_url(page),
        "next_url": get_next_url(page)
    })

@login_required(login_url='login')
def follow(request, user_to_follow):
    if request.method != POST:
        return JsonResponse({"error": "POST request required."}, status=400)

    User.objects.get(pk=request.user.id).following.add(user_to_follow)

    return redirect('profile', user_id=user_to_follow.id)


@login_required(login_url='login')
def unfollow(request, user_to_unfollow):

    if request.method != POST:
        return JsonResponse({"error": "POST request required."}, status=400)

    User.objects.get(pk=request.user.id).following.remove(user_to_unfollow)
    return redirect('profile', user_id=user_to_unfollow)

@login_required(login_url='login')
def following(request):

    following = User.objects.get(pk=request.user.id).following.all()

    following_ids = following.values_list('pk', flat=True)

    following_posts = Post.objects.filter(pk__in=following_ids)

    paginator = Paginator(following_posts, 10)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": following_posts,
        "page": page,
        "previous_url": get_previous_url(page),
        "next_url": get_next_url(page)
    })





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
