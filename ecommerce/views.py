from django.db.models import F, Q

from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from ecommerce.models import *
from ecommerce.serializers import ItemSerializer, OrderSerializer, ItemCreateSerializer


class HomeView(APIView):
    def get(self, request, *args, **kwargs) -> 'Response':
        base_url = 'http://localhost:8000/ecommerce'
        urls = {
            'Store': f'{base_url}/store/',
            'Order': f'{base_url}/<pk>/',
            'Item': f'{base_url}/item/<pk>/'
        }

        return Response(data=urls, status=status.HTTP_200_OK)


class ItemCreateAPIView(generics.CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ItemSerializer

    # @TODO: get_object

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            # @TODO: permissions

            instance = request.user.item_set.get(pk=self.get_object().pk)
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response({
                'error': "Item either doesn't exist or user has no permission"},
                status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            instance = request.user.item_set.get(pk=self.get_object().pk)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({
                'error': "Item either doesn't exist or user has no permission"},
                status=status.HTTP_400_BAD_REQUEST)


class OrderAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.request.user.order_set.all()

    def delete(self, request, *args, **kwargs) -> Response:
        order = self.get_object()
        if order.is_paid:
            return Response("can't remove already paid order", status=status.HTTP_400_BAD_REQUEST)

        Item.objects.filter(pk=order.item.pk).update(quantity=F('quantity') + 1)
        return super().delete(request, *args, **kwargs)


class CartAPIView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        pass

    def get_queryset(self):
        pass


class StoreAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
