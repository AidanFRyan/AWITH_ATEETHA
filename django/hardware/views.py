from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from datetime import datetime
from .models import Item
from .forms import SearchForm
from .searcher import Searcher
import plotly.offline as plot
import plotly.graph_objs as graph
# Create your views here.

s = Searcher()
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            l = s.searchFor(cd['query'])
            g = graph.Figure(data=graph.Scatter(x=[datetime.fromtimestamp(int(float(w['date']))) for w in l], y=[float(w['price']) for w in l]))
            p = plot.plot(g, output_type='div')
            return render(request, 'search_results.html', {'query_list': l, 'plot': p})
    else:
        form = SearchForm()
    return render(request, "home.html", {'form': form})

def searchResults(request):
    return render(request, "search_results.html")