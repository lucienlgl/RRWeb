from django.urls import path
from rrsite.view import views, user, restaurant, review

app_name = "rrsite"
urlpatterns = (
    path('', views.index, name='index'),
    path('login', user.login),
    path('logout', user.logout),
    path('register', views.register_view),

    path('email/register', user.register_email),
    path('email/verify/<str:token>', user.email_validation),
    path('phone/register', user.register_phone),

    path('forget_password', user.forget_password),

    path('api/recommend/category', restaurant.recommend_restaurant),

    path('api/review/hot', review.hot_review),

    path('api/restaurant/info', restaurant.basic_info),
    path('api/restaurant/photo', restaurant.photo_info),
    path('api/restaurant/tip', restaurant.tips_info),
    path('api/restaurant/review', restaurant.review_info),

    path('api/user/basic', user.basic_info),
)
