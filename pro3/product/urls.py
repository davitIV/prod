# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('remove_category/<int:category_id>/', views.remove_category, name='remove_category'),
]
