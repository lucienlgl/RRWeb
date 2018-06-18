from django.urls import path
from rrsite.view import views, user, restaurant, review

app_name = "rrsite"
urlpatterns = (
    path('', views.index, name='index'),
    path('login', user.login, name='login'),
    path('logout', user.logout, name='logout'),
    path('register', views.register_view, name='register'),
    path('restaurant/<str:restaurant_id>', views.restaurant_view, name='restaurant_view'),

    path('email/register', user.register_email, name='email_form'),
    path('email/verify/<str:token>', user.email_verify, name='email_verify'),
    path('phone/register', user.register_phone, name='phone_form'),
    path('forget', user.forget_password, name='forget'),

    path('user/basic', views.user_view, name='user_basic'),

    path('api/user/basic', user.basic_info, name='api_user_basic'),
    path('api/user/phone/code', user.phone_code, name='api_phone_code'),
    path('api/user/phone', user.change_phone, name='api_change_phone'),
    path('api/user/email', user.change_email, name='api_change_email'),

    path('api/restaurant/info', restaurant.basic_info, name='api_restaurant_basic'),
    path('api/restaurant/special', restaurant.special_info, name='api_restaurant_special'),
    path('api/restaurant/photo', restaurant.photo_info, name='api_restaurant_photo'),
    path('api/restaurant/tip', restaurant.tips_info, name='api_restaurant_tip'),
    path('api/restaurant/review', restaurant.review_info, name='api_restaurant_special'),

    path('api/restaurant/upload_photo', restaurant.uploadfile, name='api_restaurant_upload_photo'),

    path('api/review/hot', review.hot_review, name='api_hot_review'),

    path('api/recommend/category', restaurant.recommend, name='api_recommend_category'),
)
