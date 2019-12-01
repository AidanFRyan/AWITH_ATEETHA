from django.urls import path

from .views import search, searchResults

urlpatterns = [
    # path('search/', searchResults, name='search_results'),
    path('', search, name='home'),
]