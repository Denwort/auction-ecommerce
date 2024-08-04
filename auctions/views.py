from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Category
from django import forms

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(open=True)
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

class CreateForm(forms.Form):
    title = forms.CharField(required=True)
    descripcion = forms.CharField(widget=forms.Textarea(), required=True)
    starting_bid = forms.FloatField(required=True)
    image = forms.CharField() 
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True)

@login_required
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            descripcion = form.cleaned_data['descripcion']
            starting_bid = form.cleaned_data['starting_bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            Listing.objects.create(
                title=title,
                descripcion=descripcion,
                starting_bid=starting_bid,
                image=image,
                creator=request.user,
                category=category
            )
            return HttpResponseRedirect(reverse("index"))
    else:
        form = CreateForm()
    return render(request, "auctions/create.html", {
        "form": form
    })

def auction(request, id):
    listing = get_object_or_404(Listing, id=id)
    if request.method == "POST" and request.user.is_authenticated:
        user = request.user
        bid_amount = float(request.POST.get('bid_amount'))

        current_highest_bid = listing.bids.order_by('-amount').first()
        
        if bid_amount < listing.starting_bid:
            message = "Bid must be at least the starting bid."
        elif current_highest_bid and bid_amount <= current_highest_bid.amount:
            message = "Bid must be greater than the current highest bid."
        else:
            bid = Bid(listing=listing, user=request.user, amount=bid_amount)
            bid.save()
            message = "Bid placed successfully."
        
        return render(request, "auctions/auction.html", {
            "listing": listing,
            "watchlisted": listing in request.user.watchlist.all() if request.user.is_authenticated else False,
            "user_has_bid": (listing.bids.order_by('-amount').first() and listing.bids.order_by('-amount').first().user == request.user) if request.user.is_authenticated else False,
            "message": message,
            "comments": listing.comments.all().order_by('-created_at')
        })
    else:
        return render(request, "auctions/auction.html", {
            "listing": listing,
            "watchlisted": listing in request.user.watchlist.all() if request.user.is_authenticated else False,
            "user_has_bid": (listing.bids.order_by('-amount').first() and listing.bids.order_by('-amount').first().user == request.user) if request.user.is_authenticated else False,
            "comments": listing.comments.all().order_by('-created_at')
        })

@login_required
def toggle_watchlist(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, id=listing_id)
    if listing in user.watchlist.all():
        user.watchlist.remove(listing)
    else:
        user.watchlist.add(listing)
    return HttpResponseRedirect(reverse("auction", args=[listing_id]))

@login_required
def close(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    
    if request.user != listing.creator:
        return HttpResponseRedirect(reverse("auction", args=[listing_id]))
    
    listing.open = False
    highest_bid = listing.bids.order_by('-amount').first()
    
    if highest_bid:
        listing.winner = highest_bid.user

    listing.save()
    return HttpResponseRedirect(reverse("auction", args=[listing_id]))

@login_required
def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            comment = Comment(listing=listing, user=request.user, text=content)
            comment.save()
    
    return HttpResponseRedirect(reverse("auction", args=[listing_id]))

@login_required
def watchlist(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": watchlist
    })

def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": all_categories
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = category.listings.filter(open=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })