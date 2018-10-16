from django.shortcuts import render
from rest_framework import viewsets
from .models import CallStartRecord, CallEndRecord
from .serializers import CallStartRecordSerializer, CallEndRecordSerializer
from datetime import datetime, timedelta, tzinfo


class CallStartRecordView(viewsets.ModelViewSet):
    """Django viewSet for the CallStartRecord details receiver"""
    queryset = CallStartRecord.objects.all()
    serializer_class = CallStartRecordSerializer


class CallEndRecordView(viewsets.ModelViewSet):
    """Django viewSet for the CallEndRecord details receiver"""
    queryset = CallEndRecord.objects.all()
    serializer_class = CallEndRecordSerializer

