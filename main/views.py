from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from django_filters import rest_framework as filters

from .serializers import (ProductListSerializer, BannerListSerializer, BrandListSerializer, ProductDetailListSerializer,
                          BasketItemsCreateSerializer, CategoryCreateSerializer)
from .models import Product, Banner, Brand, Category, Storage

from .filters import ProductFilter


# @api_view(['GET'])
# def dish_list(request):
#     if request.method == 'GET':
#         dishes = Dish.objects.all()
#         serializer = DishSerializer(dishes, many=True)
#         return Response(serializer.data)


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        index_banners = Banner.objects.filter(Q(location='index_head') | Q(location='index_middle'), is_active=True)
        popular_brands = Brand.objects.all()[:4]
        best_seller_products = Product.objects.all()[:4]
        discounted_products = Product.objects.filter(new_price__isnull=False)[:4]

        index_banners_serializer = BannerListSerializer(index_banners, many=True)
        popular_brands_serializer = BrandListSerializer(popular_brands, many=True)
        best_seller_products_serializer = ProductListSerializer(best_seller_products, many=True)
        discounted_products_serializer = ProductListSerializer(discounted_products, many=True)

        data = {
            "banners": index_banners_serializer.data,
            "popular_brands": popular_brands_serializer.data,
            "best_seller_products": best_seller_products_serializer.data,
            "discounted_products": discounted_products_serializer.data,
        }

        return Response(data)


class ProductDetailView(APIView):
    @swagger_auto_schema(responses={200: ProductDetailListSerializer()})
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ProductDetailListSerializer(product)

        return Response(serializer.data)


class BasketItemsCreateView(APIView):

    def post(self, request):

        serializer = BasketItemsCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


class ProductDetailGenericView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductDetailUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
