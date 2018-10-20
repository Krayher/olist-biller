from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import CallStartRecord, CallEndRecord, QueryFilters
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
    return render(request, 'billersimple.html')


def billerCompleteReport(request, subscriber, month, year):
    """receives the subscriber, month and year to filte the report"""
    return render(request, 'billercomplete.html')


def welcome(request):
    """welcome to my app - dummie"""
    return render(request, 'welcome.html')


def list_call_by_subscriber(request, subscriber):
    qs = QueryFilters()
    qs_data = qs.get_by_subscriber(subscriber)
    endpoint = list_full_call_list(request, subscriber=subscriber, month=qs_data[0], year=qs_data[1])
    return HttpResponse([x for x in endpoint])

def list_full_call_list(request, subscriber, month, year):
    qs = QueryFilters()
    qs_data = qs.get_by_full_call_list(subscriber=subscriber, month=month, year=year)
    return HttpResponse(qs_data)

