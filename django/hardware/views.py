from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Item
from .forms import SearchForm
from .searcher import Searcher
# Create your views here.

s = Searcher()
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            l = s.searchFor(cd['query'])
            return render(request, 'search_results.html', {'query_list': l})
    else:
        form = SearchForm()
    return render(request, "home.html", {'form': form})

def searchResults(request):
    return render(request, "search_results.html")