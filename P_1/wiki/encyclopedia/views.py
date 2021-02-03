from django.shortcuts import redirect, render
from .forms import SearchForm, EntryForm, EditForm
from django.urls import reverse
import random

from . import util

search_form = SearchForm()
context = {"search_form":search_form}




def index(request):
    context["entries"] = util.list_entries()
    
    return render(request, "encyclopedia/index.html", context)



def entry(request, title):
    result = util.get_entry(title)
    if result == None:
        context["error"] = "Entry not found"
        return render(request, 'encyclopedia/error.html', context)
    else:
        context["text"] = result
        context["title"] = title
        return render(request, 'encyclopedia/entry.html', context)




def search(request, *args, **kwargs):
    if request.method == "POST":
        searched = request.POST['searched_entry']
        if util.get_entry(searched) is not None:
            return redirect(reverse("encyclopedia:entry", kwargs={'title':searched})) #if found, returns to the entry, passing along the "searched" entry into the url to go to the page of that entry
        else:
            return redirect(reverse("encyclopedia:search_results", kwargs={'searched':searched}))



def search_results(request, searched):
    entries = util.list_entries()
    context["entries"] = list(filter(lambda entry: searched.casefold() in entry.casefold(), entries)) #https://www.geeksforgeeks.org/python-finding-strings-with-given-substring-in-list/
    if not context["entries"]:
        context["error"] = f'No results for "{searched}"'
        return render(request, 'encyclopedia/error.html', context)
    else:
        context["searched"] = searched
        return render(request, "encyclopedia/search_results.html", context)



def create_page(request):
    if request.method == "GET":
        context["entry_form"] = EntryForm()
        return render(request, "encyclopedia/create_page.html", context)
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST['entry_text']
        if util.get_entry(title) is not None:
            context["error"] = "Entry already exists/Entry with that title already already exists"
            return render(request, 'encyclopedia/error.html', context)
        else:
            title.capitalize()
            util.save_entry(title, content)
            return redirect(reverse("encyclopedia:entry", kwargs={'title':title})) 


def edit_page(request, title):
    if request.method == "GET":
        if util.get_entry(title) is not None:
            content = util.get_entry(title)
            context["edit_form"] = EditForm(initial = {
                "entry_text":content})
            context["title"] = title
            return render(request, "encyclopedia/edit_page.html", context)
        else:
            context["error"] = "Entry does not exist"
            return render(request, 'encyclopedia/error.html', context)


    if request.method == "POST":
        
        content = request.POST['entry_text']
        util.save_entry(title, content)
        return redirect(reverse("encyclopedia:entry", kwargs={'title':title})) 



def random_page(request):
    
    entry_list = util.list_entries()
    random_entry = random.choice(entry_list)
    return redirect(reverse("encyclopedia:entry", kwargs={'title':random_entry})) 
