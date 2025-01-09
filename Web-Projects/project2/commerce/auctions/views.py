from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms

from .models import User, Listing, Bid, Comment, Category, WatchList

class CreateListingForm(forms.Form):
    title = forms.CharField(label='Title of listing')
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'rows':'5', 'cols':'50'}))
    bid = forms.CharField(label='Bid', widget=forms.NumberInput(attrs={'step': '0.01', 'min': '0'}))
    url = forms.CharField(label='Image_url', widget=forms.URLInput())



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
    # make a class form to display inputs on the /create_listing url page. Make it in forms.py and import it here.
    # But, I didn't do it here because I'm lazy. (But u should do it like above)

    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            url = form.cleaned_data['url']
            # To find the current user in
            user = request.user
            category = Category.objects.get(pk=request.POST['categories'])
            # Create this new list(this creating process will automatically add this new list in lists)
            Listing.objects.create(user = user, title = title, description = description, price = bid, image_url = url, category = category)

            # finally, go back to the home
            return HttpResponseRedirect(reverse('index'))

    return render(request, "auctions/create_listing.html", {
        'listing_form': CreateListingForm(),
        'categories': Category.objects.all()
    })


@login_required
def listing_info(request, listing_id):
    # Get the list looking for
    listing = Listing.objects.get(pk=listing_id)
    user = request.user
    is_owner = False
    if listing.user == user:
        is_owner = True
    category = Category.objects.get(category = listing.category)
    comments = Comment.objects.filter(listing = listing)
    watching = WatchList.objects.filter(user = user, listing = listing)

    if watching:
        watching = WatchList.objects.get(user = user, listing = listing)
    else:
        watching = WatchList.objects.create(user = user, listing = listing, watching = False)

    return listing, user, is_owner, category, comments, watching


@login_required
def listing(request, listing_id):
    info = listing_info(request, listing_id)

    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]

    # when you add comment(여기서 bidding을 제출하는것은 따로 bidding/listing_id로 따르 만들었음)
    if request.method == "POST":
        comment = request.POST('comment')
        # comment textarea에 무언가 적었다면
        if comment != "":
            Comment.objects.create(user = user, comment = comment, listing = listing)

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        # 원래 answer에서는 user 안넣었는데 여기선 넣어봄(!!! 오류있을시 빼보셈 !!!)

        'is_owner': is_owner,
        'category': category,
        'comments': comments,
        'watching': watch.watching
    })

@login_required
def remove_watchlist(request, listing_id):
    info = listing_info(request, listing_id)

    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]

    watch.watching = False
    watch.save()

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'is_owner': is_owner,
        'category': category,
        'comments': comments,
        'watching': watch.watching
    })

@login_required
def add_watchlist(request, listing_id):
    info = listing_info(request, listing_id)

    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]

    watch.watching = True
    watch.save()

    return render(request, 'auctions/listing.html', {
    'listing': listing,
    'is_owner': is_owner,
    'category': category,
    'comments': comments,
    'watching': watch.watching
    })


@login_required
def bidding(request, listing_id):
    info = listing_info(request, listing_id)
    listing, user, is_owner, category, comments, watch = info[0], info[1], info[2], info[3], info[4], info[5]

    if request.method == "POST":
        bid = request.POST['bid']
        listing.price = float(bid)
        listing.save()
        Bid.objects.create(user = user, listing = listing, price = bid)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments,
        "watching": watch,
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
        "watching": watch,
        "is_owner": is_owner,
        "is_winner": is_winner,
        "winner": winner
    })

@login_required
def watchlist(request, user_id):
    listing_ids = WatchList.objects.filter(user = request.user, watching = True).values('listing')
    listing = Listing.objects.filter(id__in = listing_ids)

    return render(request, 'auctions/watchlist.html', {
        'listings': listing
    })
