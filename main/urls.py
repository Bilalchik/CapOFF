from django.urls import path
from . import views


urlpatterns = [
    path('index/',  views.IndexView.as_view()),
    path('index/products/<int:product_id>/', views.ProductDetailView.as_view()),

    # Basket
    path('basket/create/', views.BasketItemsCreateView.as_view()),

    # Generics
    path('product_list/', views.ProductListView.as_view()),
    path('product_list/<int:pk>/', views.ProductDetailGenericView.as_view()),
    path('product_detail/<int:pk>/', views.ProductDetailUpdateView.as_view()),
    path('category/create/', views.CategoryCreateView.as_view())
]
