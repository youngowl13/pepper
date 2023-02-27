from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

import datetime
from order.models import Order
from order.serializers import OrderSerializer, OrderDetailSerializer


class OrderList(APIView, PageNumberPagination):
    page_size = 10

    def get(self, request, format=None):
        query_set = Order.objects.all()
        start_date = datetime.datetime.strptime(request.GET.get('startDate'), '%Y-%m-%d')
        end_date = datetime.datetime.strptime(request.GET.get('endDate'),  '%Y-%m-%d') + datetime.timedelta(days=1)
        if request.GET.get('restaurant'):
            query_set = query_set.filter(restaurant__ext_id=request.GET.get('restaurant'))
        query_set = query_set.filter(created__range=(start_date, end_date)).order_by('-created')
        query_set = self.paginate_queryset(query_set, request, view=self)
        serializer = OrderSerializer(query_set, many=True)
        paginated_data = self.get_paginated_response(serializer.data).data
        paginated_data['current'] = int(self.request.query_params.get('page'))
        return Response(paginated_data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message": "Success"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):

    def get_object(self, ext_id):
        try:
            return Order.objects.get(ext_id=ext_id)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, ext_id, format=None):
        order = self.get_object(ext_id)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
