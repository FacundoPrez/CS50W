from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            
            "entry": util.get_entry(title),
            "title": title
        })
    
def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    
    # Check for exact match first
    for entry in entries:
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry", args=[entry]))
    
    # If no exact match, look for substring matches
    query_lower = query.lower()
    results = [entry for entry in entries if query_lower in entry.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        if util.get_entry(title) == None:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
    else:
        return render(request, "encyclopedia/create.html")