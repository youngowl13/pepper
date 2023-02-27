from django.urls import path
from restaurant.views import RestaurantList, RestaurantDetail, RestaurantNameList, CuisineList

urlpatterns = [
    path('', RestaurantList.as_view()),
    path('cuisine/', CuisineList.as_view()),
    path('select/', RestaurantNameList.as_view()),
    path('<str:ext_id>/', RestaurantDetail.as_view()),
]
