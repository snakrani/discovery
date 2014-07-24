from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view

from vendor.models import Vendor
from api.serializers import VendorSerializer

@api_view(['GET',])
def vendor_list(request, format=None):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return  Response(serializer.data)

