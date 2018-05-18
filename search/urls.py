from django.urls import path
from search.views import *

app_name = "search"
urlpatterns = (
    path('suggest', SearchSuggest.as_view(), name='suggest'),
    path('', SearchView.as_view(), name='search'),
)
