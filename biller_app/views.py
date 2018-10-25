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

# Serialization done


@login_required
def index(request):
    """ dummie test"""
    return render(request, 'index.html')


def billerSimpleReport(request, subscriber):
    """receives the subscriber and assume last month and year end call timestamp """
    return render(request, 'billercomplete.html')


def billerCompleteReport(request, subscriber, month, year):
    """receives the subscriber, month and year to filte the report"""
    return render(request, 'billercomplete.html')


def welcome(request):
    """welcome to my app - dummie"""
    return render(request, 'welcome.html')


def find_subcriber(request, subscriber):
    """ receives the subscriber number and find the last
        period of month and year, and perform the search
        calculation and saves to @tempDataTable to display
    """
    qs = QueryFilters()
    qs_data = qs.get_interval_by_auto(subscriber=subscriber)

    # 3 Return code for missing subscriber and its filters
    # 4 Return code period not found for the provided subscriber

    if qs_data[0] in range(0, 5):
        endpoint = qs_data[1]
        context = {'info': endpoint, 'subscriber': subscriber}
        return render(request, 'billercomplete.html', context)

    else:
        endpoint = qs_data # cast for future implementations
        context = {'call_details': endpoint, 'subscriber': subscriber}
        return render(request, 'billercomplete.html', context)


def find_subscriber_month_year(request, subscriber, month, year):
    """
    :param request: (auto)
    :param subscriber: provided eg. 11970663342
    :param month: integer 2 digits
    :param year: integer 4 difits
    :return: detailed call list on screen
    """
    qs = QueryFilters()

    qs_data = qs.get_interval_by_period(subscriber=subscriber, month=month, year=year)

    if qs_data[0] in range(1, 5):
        print('ERROR DURING FILTERING')
    else:
        endpoint = qs_data # cast for future filtering implementations
        context = {'call_details': qs_data}

    return render(request, 'billercomplete.html', context)