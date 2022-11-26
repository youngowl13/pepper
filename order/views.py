from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from order.models import Order
from order.serializers import OrderSerializer, OrderDetailSerializer


class OrderList(APIView):

    def get(self, request, format=None):
        query_set = Order.objects.all()
        if request.GET.get('restaurant'):
            query_set = query_set.filter(restaurant__ext_id=request.GET.get('restaurant'))
        query_set = query_set.filter(created__range=(request.GET.get('startDate'), request.GET.get('endDate')))
        serializer = OrderSerializer(query_set, many=True)
        return Response(serializer.data)

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
