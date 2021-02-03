from django.shortcuts import redirect, render
from .forms import SearchForm
from django.urls import reverse

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
    context["entries"] = list(filter(lambda entry: searched.casefold() in entry.casefold(), entries))
    if not context["entries"]:
        context["error"] = f'No results for "{searched}"'
        return render(request, 'encyclopedia/error.html', context)
    else:
        context["searched"] = searched
        return render(request, "encyclopedia/search_results.html", context)


def create_page(request):
    return