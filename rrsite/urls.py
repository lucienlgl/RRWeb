from django.urls import path
from . import views

app_name = "rrsite"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login),
    path('register', views.register)
]
