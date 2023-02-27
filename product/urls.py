from django.urls import path
from .views import list_view, get_images, get_brands, get_categories

urlpatterns = [

    path('product-images/', get_images),
    path('brands/', get_brands),
    path('categories/', get_categories),

    path('', list_view),

]
