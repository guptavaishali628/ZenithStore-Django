
from django.urls import path
# import path
from . import views


urlpatterns = [
     path('', views.store, name='store'),
]
