from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('', views.profitable_items, name='index'),
    path('whispers/', csrf_exempt(views.whispers), name='whispers'),
    path('ooh/', csrf_exempt(views.orb_of_horizons), name='ooh'),
    path('gemExp/', csrf_exempt(views.gem_exp), name='gem_exp'),
    path('search/', csrf_exempt(views.search_resolve), name='search'),
]