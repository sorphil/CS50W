from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Max


from .models import *
from .forms import *
from django.contrib import messages



def index(request):
    listings = AuctionListing.objects.filter(active=True)
    context = {"listings":listings}
    return render(request, "auctions/index.html", context)


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


########################################
@login_required(login_url='/login')
def create(request):
    if request.method == "GET":
        return render(request, 'auctions/create.html', {"form":AuctionForm()})
    elif request.method == "POST":

        form = AuctionForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.active = True
            listing.image = form.cleaned_data.get("image")
            listing.cur_price = listing.start_bid
            listing.save()
            return HttpResponseRedirect(reverse('index'))




def listing(request, id):
    try:
        listing= AuctionListing.objects.get(id=id)
        listing_bids = Bid.objects.filter(listing=id)
        number_of_bids = listing_bids.count()
    except AuctionListing.DoesNotExist:
        raise Http404
    active = listing.active
    
    #To determine if the current user is the owner
    if listing.user.id == request.user.id:
        owner = True
    else:
        owner = False
        
    #To determine the highest bid, else if no bids, go with the starting bid
    maxbid = 0;
    lead_bidder =""
    if not listing_bids:
        maxbid = listing.start_bid
        lead_bidder = listing.user
        listing.cur_price = maxbid
        listing.save()
        
        
    else:
        for bid in listing_bids:
            if maxbid < bid.amount:
                maxbid =bid.amount
                lead_bidder=bid.user
                listing.cur_price = maxbid
                listing.save()

    #intializing forms
    commentform = CommentForm()
    #if listing is no longer active, disable form
    if active is False:
        #if listing is no longer active
        bidform = BidForm() 
        bidform.fields['amount'].disabled = True
    else:
        bidform = BidForm()

    #Obtaining all the comments on the listing
    comments = Comment.objects.filter(listing=id)
    context = {
            "bidform":bidform, #passing the highest bid as the initial/min value for a bid
            "commentform":commentform,
            "listing":AuctionListing.objects.get(pk = id),
            "maxbid":maxbid,
            "comments":comments,
            "active":active,
            "lead_bidder":lead_bidder,
            "owner":owner,
            "number_bids":number_of_bids
        }

        

    #Getting all the watchers of that listing
    watchers = listing.watchers.all()
    #To check if the user is already watching the item
    watchlist_flag = False   
    for watcher in watchers:
        if request.user.id == watcher.id:
            watchlist_flag = True
    context["watchlist_flag"] = watchlist_flag


    if request.method == "GET":
        return render(request, 'auctions/listing.html', context)

    elif request.method == "POST":
        #if user submitted the bid form
        if 'bid_submit' in request.POST:
            bidform = BidForm(request.POST)
            if int(request.POST["amount"]) <= maxbid:
                messages.error(request, f"The bid must be higher than ${maxbid}.00") 
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
            else:
                 if bidform.is_valid():
                    bid = bidform.save(commit=False)
                    bid.user = request.user
                    bid.listing_id = id
                    listing.cur_price = maxbid
                    listing.save()
                    bid.save()
                    messages.success(request, f'Bid of ${bid.amount}.00 successfully placed')
                    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))

        elif 'comment_submit' in request.POST:
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                    comment = commentform.save(commit=False)
                    comment.user = request.user
                    comment.listing_id = id
                    comment.save()
                    return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
        elif 'watchlist_submit' in request.POST:
            if watchlist_flag is False:
                listing.watchers.add(request.user.id)
                listing.save()
                messages.success(request, 'Added to watchlist')
                return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))
        
        elif 'end_submit' in request.POST:
            listing.active = False
            listing.save()
            return HttpResponseRedirect(reverse('listing', kwargs={'id': id}))


@login_required(login_url='/login')
def watchlist_view(request):
    if request.method == "GET":
        #Getting all the items watched by the user
        watched_items = AuctionListing.objects.filter(watchers=request.user.id) 
        context = {
            "watchlist":watched_items
        }
        return render(request, 'auctions/watchlist.html', context)
    elif request.method == "POST":
        listing= AuctionListing.objects.get(id=request.POST["watchlist_delete"])
        user = User.objects.get(id = request.user.id)

        #removing the user from the watcher field of the item (ie breaking the relationship)
        listing.watchers.remove(user)
        messages.success(request, f'{listing.title} removed from watchlist')
        return HttpResponseRedirect(reverse('watchlist'))
        


def categories(request):
    categories = CATEGORY_CHOICES
    for key, value in categories:
        print(value)
    context = {"categories":categories}
    return render(request, "auctions/categories.html", context)

def category(request, category):
    listings = AuctionListing.objects.filter(active=True, category = category)
    context = {"listings":listings}
    return render(request, "auctions/index.html", context)
