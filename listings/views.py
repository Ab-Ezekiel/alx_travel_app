from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Booking
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation_email

# listings/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class ListingListAPIView(APIView):
    def get(self, request):
        # sample empty response — shows up in swagger automatically
        return Response({"results": []})

