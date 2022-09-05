from django.urls import path
from restaurant.views import RestaurantList, RestaurantDetail

urlpatterns = [
    path('restaurant/', RestaurantList.as_view()),
    path('restaurant/<str:ext_id>/', RestaurantDetail.as_view()),
]
