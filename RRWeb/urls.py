from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('', include('rrsite.urls')),
    path('search/', include('search.urls')),
    path('admin/', admin.site.urls)
]