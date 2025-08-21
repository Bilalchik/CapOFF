from rest_framework import serializers
from .models import Product, Category, Brand, Banner, Size, Storage, BasketItems, Basket


class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        exclude = ('is_active', )

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'title', 'logo')


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    brands = BrandListSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'brands', 'cover', 'old_price')


class ProductDetailListSerializer(serializers.ModelSerializer):
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'brands', 'cover', 'old_price', 'description', 'new_price', 'sizes')

    def get_sizes(self, obj):
        sizes = Size.objects.all()

        result = {}
        for size in sizes:
            storage = Storage.objects.filter(product=obj, size=size, quantity__gte=1).exists()

            if storage:
                result[size.title] = {
                    "id": size.id
                }
        return result


class BasketItemsCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(write_only=True)
    size_id = serializers.IntegerField(write_only=True)
    quantity = serializers.IntegerField()
    total_price = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        basket, _ = Basket.objects.get_or_create(user=self.context['request'].user)
        product = Product.objects.filter(id=validated_data['product_id']).first()
        size = Size.objects.filter(id=validated_data['size_id']).first()

        storage_product = Storage.objects.filter(product=product, size=size).first()

        basket_items = BasketItems.objects.create(
            basket=basket,
            storage=storage_product,
            quantity=validated_data['quantity']
        )

        return basket_items


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', )
