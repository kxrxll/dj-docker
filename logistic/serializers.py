from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['quantity', 'price', 'product']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['address', 'positions']

    def validate(self, attrs):
        if not attrs['positions'][0]:
            raise ValidationError('Список пуст!')
        return attrs

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            stocks_products = StockProduct(
                stock=stock,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
            stocks_products.save()
        return stock

    def update(self, instance, validated_data):
        positions_data = validated_data.pop('positions')
        positions = instance.positions.all()
        stock = super().update(instance, validated_data)
        for position in positions_data:
            StockProduct.objects.update_or_create(
                stock=instance,
                product=position['product'],
                quantity=position['quantity'],
                price=position['price']
            )
        return stock
