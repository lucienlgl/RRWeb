from django.urls import path
from . import views

app_name = "rrsite"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login),
    path('register', views.register_view),

    path('email/register', views.register_email),
    path('email/verify/<str:token>', views.email_validation),
    path('phone/register', views.register_phone),

    path('forgot_password', views.forget_password),

    path('api/recommend/category', views.recommend_restaurant),
    path('api/review/hot', views.hot_review),
]
