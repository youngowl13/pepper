from django.urls import path
from .views import list_view, get_images

urlpatterns = [
    path('', list_view),
    path('product-images/', get_images),
    # path('<str:ext_id>/', ProductDetails.as_view()),
]
