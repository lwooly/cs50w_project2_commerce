from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django import forms

from .models import User, Auction_listing, Bid, Comment


def index(request):
    
    listing_objs = Auction_listing.objects.all().annotate(max_bid = Max('bids__bid'))
    listings = listing_objs.order_by('id')

    return render(request, "auctions/index.html", {
        "listings":listings
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


def create_listing(request):
    #for a POST request create a new listing.
    if request.method == "POST":

        # access submitted form data
        list_title = request.POST["listing_title"]
        list_description = request.POST["description"]
        list_bid = request.POST["bid"]
        list_image_url = request.POST["image_url"]
        list_category = request.POST["category"]
        user = request.user

        #save this data to the Auction model.
        listing_obj = Auction_listing(listing_title=list_title, description=list_description, image_url=list_image_url, seller=user, category=list_category)
        #get and print id of this listing obj
        listing_obj.save()
       
        #get current user to add to bid
        user = request.user

        #create starting bid
        bid_obj = Bid(bid=list_bid, listing=listing_obj, bidder=user)
        bid_obj.save()

        a = bid_obj.bid
        print(a)
        
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create_listing.html")


def listing(request, listing):

    #get listing object and related bids
    if request.method == "POST":

        listing = request.POST["post_listing_title"]
    
    #get listing object 
    listing_obj = Auction_listing.objects.filter(listing_title=listing).first()
    
    #get highest bid
    bid_obj = listing_obj.bids.order_by('-bid').first()

    #catch error where no bid
    max_bid = bid_obj.bid if bid_obj else None
    if not max_bid:
            max_bid = 0

    #set error
    error = None

    # get comments for this listing

    comments = listing_obj.listing_comments.all()

    #if form submitted via POST
    if request.method == "POST":
        if "add_comment" in request.POST:
            #create new comment
            f = Comment(comment=request.POST["add_comment"], user=request.user, listing=listing_obj)
            f.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_obj.listing_title]))
            

        if "close_listing" in request.POST:
            # seller to close listing
            # setboolean field on Auction listing model
            listing_obj.closed = True
            listing_obj.save()
            #get winning user from max bid object
            user_win = bid_obj.bidder
            # record current highest bid user in winner field on Auction listing model.
            listing_obj.winner = user_win
            listing_obj.save()
            # render page
            return HttpResponseRedirect(reverse('listing', args=[listing_obj.listing_title]))

            # show the winner of the aution.

            # if user is the winner add a specific note
        
        
        #get current user:
        user = request.user

        # get new bid
        new_bid = int(request.POST["add_bid"])

        #check that bid is higher than existing
        if new_bid > int(max_bid):
            #create new bid object:
            f=Bid(bid=new_bid, listing=listing_obj, bidder=user)
            f.save()
    
            return HttpResponseRedirect(reverse('listing', args=[listing_obj.listing_title]))

        else:
            # invalid numerical entry
            error = "Error: Enter a bid higher than the current"
              
    return render(request, "auctions/listing.html", {
        "listing":listing_obj,
        "max_bid":max_bid,
        "error":error,
        "comments": comments
    })


def watchlist(request):
    
    if request.method =="POST":
        #get user object
        user = request.user

        #find the listing.id from the submitted form
        listing_id = int(request.POST["listing_id"])

        #find listing from id
        listing = Auction_listing.objects.get(pk=listing_id)

        if "add_watchlist_item" in request.POST:
            #add the listing to the watchlist
            user.watchlist.add(listing)

        elif "remove_watchlist_item" in request.POST:
            user.watchlist.remove(listing)

        return HttpResponseRedirect(reverse("watchlist"))

    else:
        #get current user
        user = request.user
        #get watchlist for current user
        watchlist = user.watchlist.all().annotate(max_bid = Max('bids__bid'))
        return render(request, "auctions/watchlist.html", {
            "watchlist":watchlist
        })
    

def categories(request):
    # show a list of unique categories in the project
    listing_objs = Auction_listing.objects.all()
    categories = []
    for listing_obj in listing_objs:
        category = listing_obj.category
        if category not in categories:
            categories.append(category)

    return render(request, "auctions/categories.html", {
        "categories":categories
    })



# create a list of strings from the Auction_objs

def category(request, cat):
    #get all Auction listings with this category
    cat_listings = list(Auction_listing.objects.filter(category=cat))
    print(cat_listings)
    return render(request, "auctions/category.html", {
        "listings":cat_listings
    })