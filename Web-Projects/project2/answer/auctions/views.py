from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment, Category, WatchList
from .forms import CreateListingForm

##  문제점들!!!!
# 1. remove from watchlist를 누르고 다시 home으로 가서 그 remove한 아이템에 가보면
# add to cart라고 되어있어야되는데 remove from watchlist로 되어있음.(7/29일에 해결완료)
# 2.


def index(request):
    return render(request, "auctions/index.html",
    {"listings": Listing.objects.filter(sold=False)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            image_url = form.cleaned_data["image_url"]
            user = request.user
            category_id = Category.objects.get(id=request.POST["categories"])
            Listing.objects.create(user = user, title = title, description = description,
            price = bid, image_url = image_url, category = category_id)

        return HttpResponseRedirect(reverse('index'))

    else:
        return render(request, "auctions/create_listing.html", {
            "listing_form": CreateListingForm(),
            "categories": Category.objects.all()
        })

@login_required
def listing_info(request, listing_id):
    # https://citylock77.tistory.com/82 obejcts.get()과 objects.filter()의 차이점
    listing = Listing.objects.get(id=listing_id)
    user = request.user
    is_owner = True if listing.user == user else False
    category = Category.objects.get(category=listing.category)

    # 이건 lecture4에서 인용한거임. 여기서 test1은 Airport오브젝트인 test1 = Airport.objects.get(city="New York")
    #         >>> test1
    #         <Airport: New York (JFK)>
    #         >>> Flight.objects.filter(origin=test1.code)
    #         ValueError: Field 'id' expected a number but got 'JFK'.
    #         >>> Flight.objects.filter(origin=test1.id)
    #       <QuerySet [<Flight: 2: New York (JFK) to Paris (CDG)>]>
    # 한마디로 이렇게 테스트를 해본결과 같은 parameter가 아닌 id를 대신 넣으면(넣은값인 test1자체는 origin 과 같은 오브젝트인 Airport이기 때문에 ) 같은 오브젝트라는 전제하에 통과가됨.
    # ㅋㅋㅋㅋ 근데 그냥 listing.id 대신 listing넣어도됨. 이새키 왜 이렇게 만들었노

    comments = Comment.objects.filter(listing=listing.id)
    watching = WatchList.objects.filter(user = user, listing = listing)
    if watching:
        # 이렇게 하는 이유는 filter는 Query set을 항상 주기 때문인데 만약에 이게 존재한다면 get()으로 정확한 list '하나'를 가져온다.(만약 리스트가 조건에 부합하는게 여러갠데 get()을 사용하면 error.)
        watching = WatchList.objects.get(user = user, listing = listing)
    else:
        watching = WatchList.objects.create(user = user, listing = listing, watching = False)

    # this returns a list like [listing, user, is_owner, ....]
    return listing, user, is_owner, category, comments, watching

@login_required
def listing(request, listing_id):
    info = listing_info(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]

    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            Comment.objects.create(user = user, listing = listing, comment = comment)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments,  # Comment.objects.filter(listing=listing.id)
        "watching": watch.watching,   # WatchList.objects.get(user = user, listing = listing).watching
        "is_owner": is_owner
    })

@login_required
def remove_watchlist(request, listing_id):
    info = listing_info(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    watch.watching = False
    watch.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments,
        "watching": watch.watching,
        "is_owner": is_owner
    })

@login_required
def add_watchlist(request, listing_id):
    info = listing_info(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    # watch = WatchList.objects.filter(user = user, listing = listing)
    # if watch:
    #     watch = WatchList.objects.get(user = user, listing = listing)
    #     watch.watching = True
    #     watch.save()
    # else:
    #     WatchList.objects.create(user = user, listing = listing, watching = True)

    # 지금 코맨트 해놓은게 원래꺼고 지금게 내가 수정해본것
    watch.watching = True
    watch.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments,
        # "watching": WatchList.objects.get(user = user, listing = listing).watching,
        "watching": watch.watching,
        "is_owner": is_owner
    })

@login_required
def bidding(request, listing_id):
    info = listing_info(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    if request.method == "POST":
        bid = request.POST["bid"]
        listing.price = float(bid)
        listing.save()
        Bid.objects.create(user = user, price = bid, listing = listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments,
        "watching": watch.watching,
        "is_owner": is_owner
    })

@login_required
def close_bidding(request, listing_id):
    info = listing_info(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]
    listing.sold = True
    listing.save()
    winner = Bid.objects.get(price = listing.price, listing = listing).user
    print(user.id, winner.id)
    is_winner = user.id == winner.id

    return render(request, "auctions/close_bidding.html", {
        "listing": listing,
        "category": category,
        "comments": comments,
        "watching": watch.watching,
        "is_owner": is_owner,
        "is_winner": is_winner,
        "winner": winner
    })

@login_required
def watchlist(request, user_id):
    listing_ids = WatchList.objects.filter(user = request.user, watching=True).values('listing')
    # id__in에 대한 설명. 쉽게 말하면 Where id in [1,2,3] -> id가 1이나 2나 3인것. https://jinmay.github.io/2020/05/25/django/django-values-and-values-list/
    # list, tuple, string 또는 queryset과 같이 iterable한 객체를 대상으로 각 원소를 조회합니다
    # 여기서는 listing_ids가 <QuerySet [{'listing': <Flight: 1: Paris (CDG) to Tokyo (NRT)>}, {...}, {...}]> 이런식일텐데 id__in을 사용하여 각 dict의 'listing' 값의 id를 조회.
    listing = Listing.objects.filter(id__in = listing_ids)
    return render(request, "auctions/watchlist.html", {
        "listings": listing
    })

def category(request):
    listings = None
    category = None
    if request.method == "POST":
        category = request.POST["categories"]
        listings = Listing.objects.filter(category = category)
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
        "category": Category.objects.get(id = category).category if category is not None else "",
        "listings": listings
    })



# 정보들
# 1. obejcts.get()과 objects.filter()의 차이점 - https://citylock77.tistory.com/82
# 2. objects.filter은 Queryset을 주는데 <QuerySet [<Flight: 1: New York to London>]>. 저 Queryset안에 있는것이 object임(이상황에선 하나 밖에없음)
# 3. objects.values()는 무엇인지 https://jinmay.github.io/2020/05/25/django/django-values-and-values-list/
# 4. filter(id__in)에 대한 설명 https://jinmay.github.io/2020/05/25/django/django-values-and-values-list/
# 5.