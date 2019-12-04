from django.urls import path

from .views import search, searchResults, confirmDelete

urlpatterns = [
    path('search/', searchResults, name='search_results'),
    path('', search, name='home'),
    path('confirmDelete/', confirmDelete, name='confirm')
]