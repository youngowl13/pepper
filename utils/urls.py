from django.urls import path
from utils.views import CityList

urlpatterns = [
    path('city', CityList.as_view()),
]
