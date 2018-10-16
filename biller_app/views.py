from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import CallStartRecord, CallEndRecord
from .serializers import CallStartRecordSerializer, CallEndRecordSerializer
from datetime import datetime, timedelta, tzinfo
from django.contrib.auth.decorators import login_required


class CallStartRecordView(viewsets.ModelViewSet):
    """Django viewSet for the CallStartRecord details receiver"""
    queryset = CallStartRecord.objects.all()
    serializer_class = CallStartRecordSerializer


class CallEndRecordView(viewsets.ModelViewSet):
    """Django viewSet for the CallEndRecord details receiver"""
    queryset = CallEndRecord.objects.all()
    serializer_class = CallEndRecordSerializer

################################## Serialization done


@login_required
def index(request):
    """ dummie test"""
    return render(request, 'index.html')


def billerSimpleReport(request, subscriber):
    """receives the subscriber and assume last month and year end call timestamp """
    return HttpResponse('Simple Report Rendering taking place...')


def billerCompleteReport(request, subscriber, month, year):
    """receives the subscriber, month and year to filte the report"""
    return HttpResponse('Complete Report Rendering taking place...')