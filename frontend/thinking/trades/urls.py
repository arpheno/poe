from django.urls import path

from . import views

urlpatterns = [
    path('', views.profitable_items, name='index'),
]