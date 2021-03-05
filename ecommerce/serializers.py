from ecommerce.models import *
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Tag


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        exclude = ('item',)


class ItemSerializer(serializers.ModelSerializer):
    tag = serializers.ListSerializer(child=serializers.CharField(source='tag.title'))
    images = ImageSerializer(many=True, source='itemimage_set')

    class Meta:
        model = Item
        fields = ('id', 'name', 'quantity', 'price', 'available', 'tag', 'images')


class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('user',)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
