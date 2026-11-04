from django.urls import path
from .import views

urlpatterns = [
    path('', views.cart, name='cart'),
    # path for increment
    path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
    # path for decrement
    path('remove_cart/<int:product_id>/', views.remove_cart, name='remove_cart'),
    # path for remove cart item
    path('remove_cart_item/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),

]
