from django.shortcuts import render
from django.http import JsonResponse
import time
# Create your views here.
def index(request):
    return render(request, 'posts/index.html')


#Data is fetched from this url, ie this function
def post(request):

    #Get starting and end point
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    #Generate list of posts
    data = []
    for i in range(start, end + 1):
        data.append(f"Post #{i}")

    
    #Artifically delay speed
    time.sleep(1)

    return JsonResponse({
        "posts": data
    })