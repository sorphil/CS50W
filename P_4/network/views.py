import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt    
from django.http import JsonResponse
from django.contrib import messages
from .serializers import ProfileSerializer
from .serializers import UserPostSerializer



from .models import User
from .forms import *

def index(request):
    if request.method == "GET":
        context = {}
        if request.user.is_authenticated:
            posts = UserPost.objects.all()
            context = {
                "postform":UserPostForm(),
            }
        return render(request, "network/index.html", context)
    elif request.method == "POST" and "postformsubmit" in request.POST:
        if request.user.is_authenticated:
            postForm = UserPostForm(request.POST)
            if postForm.is_valid():
                post = postForm.save(commit=False)
                post.text = postForm.cleaned_data['text']
                post.user = request.user
                post.pub_date = datetime.now()
                post.save()
                return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("login"))
                
            

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
        profile = Profile.objects.create(user = user)
        profile.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def load_posts_index(request):
    if request.method == "GET":
        posts = UserPost.objects.all().order_by("-pub_date")
        serializer = UserPostSerializer(posts, many=True)
        data = serializer.data
        data.append({"current_user":request.user.pk, "current_username":request.user.username})
        return JsonResponse(data, safe=False)

@login_required
@csrf_exempt
def likepost(request, post_id):
    if request.user.is_authenticated:  
        if request.method == "PUT":
            post = UserPost.objects.get(pk = post_id)
            
            current_user = post.likes.filter(id = request.user.id)
            if current_user.exists():  
                    post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
                
            return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse("login"))



def profile_index(request, user_name):
    user = User.objects.filter(username = user_name).first()
    if not user:
        messages.error(request, f"User {user_name} does not exist") 
        return HttpResponseRedirect(reverse('index'))
    return render(request, "network/profile.html")
    


def profile_load(request, user_name):
    
    user = User.objects.filter(username = user_name).first()  
    if not user:
        messages.error(request, f"User {user_name} does not exist") 
        return HttpResponseRedirect(reverse('index'))

    profile = Profile.objects.get(user= user)
    if request.method == "GET":
        serializer = ProfileSerializer(profile, many = False)
        data = serializer.data
        return JsonResponse(data, safe = False)        

@login_required
@csrf_exempt
def follow_unfollow(request, user_name):
    if request.user.is_authenticated:  
        #user = user of profile, profile = profile of user, cur_user_profile = profile of the loggedin user
        user = User.objects.filter(username = user_name).first()

        if not user:
            messages.error(request, f"User {user_name} does not exist") 
            return HttpResponseRedirect(reverse('index'))

        profile = Profile.objects.get(user= user)
        cur_user_profile = Profile.objects.get(user= request.user)
        if request.method == "PUT":
            if request.user in profile.followers.all():
                profile.followers.remove(request.user)
                cur_user_profile.following.remove(user)
            else:
                profile.followers.add(request.user)
                cur_user_profile.following.add(user)
            return HttpResponse(status=204)
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse("login"))


def following_index(request):
    if request.user.is_authenticated:
        return render(request, "network/following.html")
    else:
        return HttpResponseRedirect(reverse("login"))


def following_load(request):
    User = Profile.objects.get(user = request.user)
    following = User.following.all()
    user_ids = [following_user.id for following_user in following] # puts the users (their ids) being followed by the current user in a list
    posts = UserPost.objects.filter(user__id__in = user_ids).order_by('-pub_date') # filter Userpost object using user__id__in to search the list
    serializer = UserPostSerializer(posts, many=True)
    data = serializer.data
    data.append({"current_user":request.user.pk, "current_username":request.user.username})
    return JsonResponse(data, safe=False)


@login_required
@csrf_exempt
def edit_post(request, post_id):
    try:
        post = UserPost.objects.get(pk = post_id)
    except UserPost.DoesNotExist:
        messages.error(request, f"Post {post_id} does not exist") 
        return HttpResponseRedirect(reverse('index'))

    if request.user.is_authenticated:
        if request.method == "PUT":
            data = json.loads(request.body)
            post.text = data["text"]
            post.pub_date = datetime.now()
            post.save()
            return HttpResponse(status=204)
    else:
        return HttpResponseRedirect(reverse("login"))
