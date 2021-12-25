from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from .models import User, Category, Listing, Comment, Bid

from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return render(request, "auctions/index.html", {
        'auctions': Listing.objects.all()
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

# Create a new listing
@login_required(login_url='/login')
def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        seller = request.user
        discription = request.POST['discription']
        image = request.POST['image']
        price = request.POST['price']
        category = Category.objects.get(pk=request.POST['category'])

        data = Listing(title=title, seller=seller, discription=discription,
                       image=image, price=price, category=category)
        data.save()
        return render(request, 'auctions/create.html', {
            'title': title,
            'alert': True,
            'categories': Category.objects.all()
        })
    return render(request, 'auctions/create.html', {
        'categories': Category.objects.all()
    })


# Show listings by ID | Comments | Place Bid
def listing(request, listing_id):
    # Get the specific listing by its ID
    listing = Listing.objects.get(pk=listing_id)
    user = request.user

    if request.method == 'POST':

        # Comment Form
        if 'comment' in request.POST:
            comment = request.POST['comment']

            new_comment = Comment(content=comment, user=user, listing=listing)
            new_comment.save()
            # Save the comment, redirect and jump to comments section.
            return HttpResponseRedirect(reverse('listing', args=(listing_id,)) + '#comments')

        # Bid Now Form
        if 'bid_now' in request.POST:
            current_price = listing.price
            new_bid = float(request.POST['bid_now'])

            # if the new bid value is valid, update listing data (Current price and the best bidder)
            if new_bid > current_price:
                listing.price = new_bid
                listing.best_bidder = user
                listing.save()
                # Save the Bid to Database
                Bid(user=user, listing=listing, amount=new_bid).save()
                return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
            else:
                return render(request, 'auctions/listings.html', {
                    'listing': listing,
                    'comments': listing.comments.all(),
                    'watched_auctions': Listing.objects.filter(watchers__username=user),
                    'bids_count': listing.bids.all().count,
                    'alert': "* The bid must be greater than the current price!"
                })

    return render(request, 'auctions/listings.html', {
        'listing': listing,
        'comments': listing.comments.all(),
        'bids_count': listing.bids.all().count,
        'watched_auctions': Listing.objects.filter(watchers__username=user)
    })


# Watchlist Page view
@login_required(login_url='/login')
def watchlist(request):
    user = request.user
    # Get all auctions that contains [user] in its watchers list.
    watched_auctions = Listing.objects.filter(watchers__username=user)
    return render(request, 'auctions/watchlist.html', {
        'watched_auctions': watched_auctions,
        'number': watched_auctions.count
    })


# Add to watchlist
@login_required(login_url='/login')
def watchlist_add(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        listing.watchers.add(request.user)
        listing.save()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))

# Remove from watchlist
@login_required(login_url='/login')
def watchlist_remove(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        listing.watchers.remove(request.user)
        listing.save()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))


# Categories Page:
def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })


# Filter auctions by Categories:
def category(request, listing_cat):
    try:
        category = Category.objects.get(name=listing_cat)

        return render(request, 'auctions/category.html', {
            'category': category,
            'auctions': category.cat_listings.all()
        })
    # if the query does not exist, Redirect to categories page
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('categories'))


# Close an auction
@login_required(login_url='/login')
def close(request, listing_id):
    if request.method == 'POST':
        # Get the auction
        listing = Listing.objects.get(pk=listing_id)
        # update its active status and save it
        listing.active = False
        listing.save()
    return HttpResponseRedirect(reverse('listing', args=(listing_id,)))
