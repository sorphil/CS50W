from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse


class NewTaskForm(forms.Form):
    task = forms.CharField(label = "New Task")

# Create your views here.

def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html",{
        "tasks":request.session["tasks"] 
        })

def addtask(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"].append(task)
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
             return render(request, "tasks/addtask.html",{
        "form": form
    })


    return render(request, "tasks/addtask.html",{
        "form": NewTaskForm()
    })