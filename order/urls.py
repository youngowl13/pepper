from django.urls import path

from order.views import OrderList, OrderDetail

urlpatterns = [
    path('', OrderList.as_view()),
    path('<str:ext_id>/', OrderDetail.as_view())
]
