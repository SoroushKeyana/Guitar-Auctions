from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, render

from .models import User, Category, AuctionListing, Comment, Bid


def index(request):
    categories = Category.objects.all()
    active_listings = AuctionListing.objects.filter(is_active=True).order_by('-created_date')
    return render(request, "auctions/index.html", {'active_listings': active_listings, 'categories': categories})

def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    active_listings = AuctionListing.objects.filter(is_active=True, category=category)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "current_category": category.name
    })

def categories_page(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def comment(request, id):
    current_user = request.user
    listing_data = AuctionListing.objects.get(pk=id)
    message = request.POST['comment']
    comment = Comment(author = current_user, listing = listing_data, message = message)

    comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))

def bid(request, id):
    newBid = float(request.POST['newBid'])
    listing_data = AuctionListing.objects.get(pk=id)
    isListingInWatchlist = request.user in listing_data.watchlist.all()
    is_owner = request.user.username == listing_data.owner.username
    comments = Comment.objects.filter(listing=listing_data)
    if newBid > listing_data.price.bid:
        updateBid = Bid(user=request.user, bid=newBid)
        updateBid.save()
        listing_data.price = updateBid
        listing_data.save()
        return render(request, "auctions/listing.html", {"listing": listing_data, "message": "Bid placed successfully!", "update": True, "isListingInWatchlist": isListingInWatchlist, "is_owner": is_owner, "comments": comments})
    else:
        return render(request, "auctions/listing.html", {"listing": listing_data, "message": "Something went wrong.", "update": False, "isListingInWatchlist": isListingInWatchlist, "is_owner": is_owner, "comments": comments})
    
def listing(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    isListingInWatchlist = request.user in listing_data.watchlist.all()
    comments = Comment.objects.filter(listing=listing_data).order_by('-created_date')
    is_owner = request.user.username == listing_data.owner.username

    if not listing_data.is_active and request.user == listing_data.price.user:
        if not isListingInWatchlist:
            listing_data.watchlist.add(request.user)
            isListingInWatchlist = True

    return render(request, "auctions/listing.html", {
        "listing": listing_data, 
        "isListingInWatchlist": isListingInWatchlist, 
        "comments": comments,
        "is_owner": is_owner
    })

def my_listings(request):
    current_user = request.user
    status = request.GET.get('status', 'active')
    
    if status == 'active':
        active_listings = AuctionListing.objects.filter(owner=current_user, is_active=True)
        closed_listings = []  
    else: 
        active_listings = []
        closed_listings = AuctionListing.objects.filter(owner=current_user, is_active=False)
    
    return render(request, "auctions/my_listings.html", {
        "active_listings": active_listings,
        "closed_listings": closed_listings,
        "status": status 
    })


def end_auction(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    listing_data.is_active = False
    listing_data.save()
    comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listing_data, 
        "message": "Auction ended successfully",
        "comments": comments,
        "is_owner": is_owner,
        "update": True,
    })


def create_listing(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, "auctions/create_listing.html", {'categories': categories})
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = float(request.POST["price"]) 
        category_name = request.POST["category"]
        user = request.user

        category_data = Category.objects.get(name=category_name)

        initial_bid = Bid(bid=price, user=user)
        initial_bid.save()

        auction_listing = AuctionListing(
            title=title,
            description=description,
            image_url=image_url,
            price=initial_bid,
            category=category_data,
            owner=user
        )
        auction_listing.save()  

        return HttpResponseRedirect(reverse("index"))


def display_watchlist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    current_user = request.user
    listings = current_user.watchlist.all()
    return render(request, "auctions/watchlist.html", {'active_listings': listings})

def add_watchlist(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def remove_watchlist(request, id):
    listing_data = AuctionListing.objects.get(pk=id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

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
