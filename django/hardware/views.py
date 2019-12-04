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
    form = SearchForm()
    return render(request, "home.html", {'form': form})

def searchResults(request):
    if request.POST:
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            l = s.searchFor(cd['query'])
            g = graph.Figure(data=graph.Scatter(x=[datetime.fromtimestamp(int(float(w['date']))) for w in l['q']], y=[float(w['price']) for w in l['q']]))
            p = plot.plot(g, output_type='div')
            return render(request, 'search_results.html', {'query_list': l, 'plot': p})

def confirmDelete(request):
    if request.POST:
        if 'deletion' in request.POST:
            s.removeFromQueries(request.POST['pid'], request.POST['qstr'].split())
        elif 'correction' in request.POST:
            s.updateInQueries(request.POST['pid'], request.POST['qstr'].split(), float(request.POST['correctedPrice']))
            return redirect('/')
    return render(request, "delete.html", {'delete': request.POST['pid']})