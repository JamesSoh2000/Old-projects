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

# Everyone can see all posts
def index(request):

    posts = Post.objects.all()
    # Pagination(Page navigation)을 검색 https://ssungkang.tistory.com/entry/Django-11-Pagination-%EC%9D%84-%EC%95%8C%EC%95%84%EB%B3%B4%EC%9E%90
    # Paginator(객체들, 한페이지에 담길 수) 2개의 인자를 받는데 첫 번째로 페이지로 분할될 객체, 두 번째로 한 페이지에 담길 객체의 수를 받습니다.
    paginator = Paginator(posts, 10)

    # Gets page number from query string in URL '?page=' and if not, defaults to 1
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

    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Query for requested post
    try:
        post = Post.objects.get(pk = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # User requesting to edit must be the author
    if request.user == post.author:
        # Decodes the request to pull out the 'content'
        # Django에서 POST 응답의 data 받기방법
        # 여기 아래 3줄을 그냥 request.POST.get('content') 한줄로 끝낼수 있음(원래라면? 근데 지금안됨 9/1)
        # print(request.POST.get('content')) -> 아무것도안나옴(None)
        # print(request.body) -> b'{"content":"Lmaoffagasf"}'
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        content = body['content']

        # print(request.body)
        # Updates post with new content
        # How to use filter.update() https://jinmay.github.io/2020/05/13/django/django-queryset-update/
        # 여기서 filter().update()를 하게 되면 Queryset 안의 모든 objects들의 content를 update하는것임, 그런데 이 상황에선 Queryset에 object하나만 있었기 때문에 이게 가능
        # 아래 3줄이 하나의 object만 특정해서 update하는 방법
        # re = Post.objects.get(pk=post_id)
        # re.content = content
        # re.save()

        Post.objects.filter(pk=post_id).update(content=f'{content}')
        # print(Post.objects.filter(pk=post_id)) -> <QuerySet [<Post: arnell14 posted ff>]>
        # print(Post.objects.get(pk=post_id)) -> arnell14 posted ff

        # Returns Json Response with content passed back that we can use with JS to update page

        # 이렇게 editpost/post_id path를 치면 아래처럼 {'message': asdf, 'content': asdfa1} 같은 json 페이지로 가게됨.
        return JsonResponse({"message": "Post updated successfully.", "content": content}, status=200)

    else:
        return JsonResponse({"error": "You do not have permission to do this"}, status=400)


@csrf_exempt
@login_required
def updatelike(request, post_id):

    # Saves user and post from the request
    user = request.user

    # Query for requested post
    try:
        post = Post.objects.get(pk = post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    # If the user has liked the post, unlike it
    # user.likes is possible. 왜나면 models.py를 가보면 Post의 모델에 liked_by를 User와 related_name = 'likes'로 연결해 놓아 User도 사용가능.
    if (user.likes.filter(pk=post_id).exists()):
        post.liked_by.remove(user)
        likes_post = False
    # If the user doesn't like the post, like it
    else:
        post.liked_by.add(user)
        likes_post = True

    # Save updated no of likes on post
    # print(post.likes()) -> 2  이런식으로 like을 누르면 그 post의 like 수를 보여줌.
    # 하지만 print(post.likes) -> <bound method Post.likes of <Post: arnell14 posted is it post?sfg>> 라고 나옴
    likes = post.likes()

    # 이렇게 updatelike/post_id path를 치면 아래처럼 {'likePost': asdf, 'likesCount': asdfa1} 같은 json 페이지로 가게됨.
    return JsonResponse({"likesPost": likes_post, "likesCount": likes}, status=200)

@login_required
def newpost(request):

    # Writing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Takes form from POST request
    # https://wayhome25.github.io/django/2017/05/06/django-model-form/
    form = NewPostForm(request.POST)

    # Checks if form is valid, saves new post to database and redirects user to "posts"
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return HttpResponseRedirect(reverse("index"))
        # 위에 대신 return redirect('index') 가능

def profile(request, user_id):

    # Looks up user of profile
    profile_user = User.objects.get(pk = user_id)

    # Searches for relevant posts and separate posts into pages of 10
    # 여기서 profile_posts = Post.objects.filter(pk=user_id)를 하면 되자않나? 라고 생각했지만 여기서 각 Post objects들은 각각의 id들로 구성되있어 저의미는 user_id가 2라고 하면 2번째 object를 가져오라는 뜻이되버림.
    profile_posts = Post.objects.filter(author=user_id)
    paginator = Paginator(profile_posts, 10)

    # Gets page number from query string in URL '?page=' and if not, defaults to 1
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    # Flag that tells you if logged in user is following this user
    # request.user.is_authenticated 의미는 누군가의 profile을 보고있는 유저가 login을 했는지 체크. 안했을경우 follow나 unfollow기능은 사용불가.
    # 여기서 following을 체크하는 이유는 만약 로그인한 유저가 프로파일의 유저를 팔로우하고있을 경우 unfollow하거나 follow를 할수 있게 하기위해서
    if request.user.is_authenticated:
        # I guess I can use filter like this, not only using for objects.filter
        following = profile_user.followers.filter(id = request.user.id).exists()
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

    # Following a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Adds 'user_to_follow' to user's following list
    User.objects.get(pk=request.user.id).following.add(user_to_follow)
    # Reloads 'user_to_follow's page
    # return HttpResponseRedirect(reverse("profile", args=(user_to_follow,)))
    return redirect('profile', user_id=user_to_follow)

@login_required(login_url='login')
def unfollow(request, user_to_unfollow):

    # Unfollowing a user must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Removes 'user_to_follow' from user's following list
    User.objects.get(pk=request.user.id).following.remove(user_to_unfollow)
    # Reloads 'user_to_follow's page
    # return HttpResponseRedirect(reverse("profile", args=(user_to_unfollow,)))
    return redirect('profile', user_id=user_to_unfollow)

@login_required(login_url='login')
def following(request):

    # Makes a query to find who the logged in user is following
    # print(following) -> <QuerySet [<User: justlikethat17>, <User: sky1>]>
    following = User.objects.get(pk=request.user.id).following.all()

    # Creates a list of ids, which we will use in the 'following_posts' query below
    # django Querset.values()와 Queryset.values_list 사용법 https://jinmay.github.io/2020/05/25/django/django-values-and-values-list/
    following_ids = following.values_list('pk', flat=True)  # arnell14로 로그인한 기준 <QuerySet [1, 3]> 이뜻은 사용자 2명 following중.

    # Filters to only show posts that the logged in user follows
    # how to use filter(__in)  https://stackoverflow.com/questions/8618068/django-filter-queryset-in-for-every-item-in-list
    # 이뜻이 뭐냐면 author 아이디들 안에 following_ids에 해당하는 아이디들을 뜻하는것. 여기서는 author아이디가 1이나 3인 모든 Post들.
    following_posts = Post.objects.filter(author__in=following_ids)

    # Creates paginator object that separates posts into pages of 10
    paginator = Paginator(following_posts, 10)

    # Gets page number from query string in URL '?page=' and if not, defaults to 1
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
            messages.error(request, 'Invalid username and/or password.')
            return render(request, "network/login.html")
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
            messages.error(request, 'Passwords must match.')
            return render(request, "network/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, 'Username already taken.')
            return render(request, "network/register.html")

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# 여러 소스들
# django Querset.values()와 Queryset.values_list 사용법 https://jinmay.github.io/2020/05/25/django/django-values-and-values-list/
# how to use filter(__in)  https://stackoverflow.com/questions/8618068/django-filter-queryset-in-for-every-item-in-list 자세한건 207줄로