
from django.urls import path
# import path
from . import views


urlpatterns = [
     path('', views.store, name='store'),
     # create urls for products by categpories
     path('category/<slug:category_slug>/', views.store, name='products_by_category'),
]
