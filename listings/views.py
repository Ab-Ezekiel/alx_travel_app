from django.shortcuts import render

# listings/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class ListingListAPIView(APIView):
    def get(self, request):
        # sample empty response — shows up in swagger automatically
        return Response({"results": []})

