
from django.urls import path
# import path
from . import views


urlpatterns = [
     path('', views.store, name='store'),
     # create urls for products by categpories
     path('category/<slug:category_slug>/', views.store, name='products_by_category'),
     # create urls for product details
     path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
     # path for search
     path('search/', views.search, name='search'),

]
