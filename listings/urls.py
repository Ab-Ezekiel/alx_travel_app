# listings/urls.py
from django.urls import path
from .views import ListingListAPIView

urlpatterns = [
    path("listings/", ListingListAPIView.as_view(), name="listings-list"),
]
