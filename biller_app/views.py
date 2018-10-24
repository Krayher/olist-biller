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
    return render(request, 'billercomplete.html')


def billerCompleteReport(request, subscriber, month, year):
    """receives the subscriber, month and year to filte the report"""
    return render(request, 'billercomplete.html')


def welcome(request):
    """welcome to my app - dummie"""
    return render(request, 'welcome.html')


def find_subcriber(request, subscriber):
    qs = QueryFilters()

    qs_data = qs.get_interval_by_auto(subscriber)


    #endpoint = "Subscriber not found, check phone number and try again."
    #endpoint = qs.get_by_full_call_list(subscriber=subscriber,
    #                                    month=qs_data.closed_period_month,
    #                                    year=qs_data.closed_period_year)
    context = {

        'call_details': "x"
    }

    print(context)

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

    if qs_data == 1:
        print('ERROR DURING FILTERING')

    context = {

        'call_details': qs_data
    }

    return render(request, 'billercomplete.html', context)

