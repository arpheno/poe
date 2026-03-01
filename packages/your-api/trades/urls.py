from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", views.profitable_items, name="index"),
    path("whispers/", csrf_exempt(views.whispers), name="whispers"),
    path("ooh/", csrf_exempt(views.orb_of_horizons), name="ooh"),
    path("gemExp/", csrf_exempt(views.gem_exp), name="gem_exp"),
    path("gemVaal/", csrf_exempt(views.gem_vaal), name="gem_vaal"),
    path("search/", csrf_exempt(views.search_resolve), name="search"),
    path("regradingLens/", csrf_exempt(views.regrading_lens), name="regrading_lens"),
    path("directWhisper/", csrf_exempt(views.direct_whisper), name="direct_whisper"),
]
