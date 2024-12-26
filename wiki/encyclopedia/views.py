import random
import markdown2

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        html_content = markdown2.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "entry": html_content,
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
        
        if util.get_entry(title) is None:
            # Prepend title as markdown h1 header
            markdown_content = f"# {title}\n\n{content}"
            util.save_entry(title, markdown_content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "An entry with this title already exists."
            })
    else:
        return render(request, "encyclopedia/create.html")
        
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "The requested page was not found."
            })
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content  
        })
    
def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[title]))