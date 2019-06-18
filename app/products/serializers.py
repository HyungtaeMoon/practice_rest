from rest_framework import serializers

from .models import Product


# class ProductSerializer(serializers.Serializer):
#     pk = serializers.IntegerField(read_only=True)
#     description = serializers.CharField(max_length=100)
#     price = serializers.DecimalField(max_digits=9, decimal_places=2)
#     quantity = serializers.IntegerField()
#
#     def create(self, validated_data):
#         """
#         검증한 데이터로 새 'Product' 인스턴스를 생성하여 리턴
#         """
#         return Product.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         검증한 데이터로 기존 'Product' 인스턴스를 업데이트한 후 리턴
#         """
#         instance.description = validated_data.get('description', instance.description)
#         instance.price = validated_data.get('price', instance.price)
#         instance.quantity = validated_data.get('quantity', instance.quantity)
#         instance.save()
#         return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'description', 'price', 'quantity')
