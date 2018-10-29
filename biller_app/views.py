from django.shortcuts import render
from rest_framework import viewsets
from .models import CallStartRecord, CallEndRecord, QueryFilters
from .serializers import CallStartRecordSerializer, CallEndRecordSerializer
from django.contrib.auth.decorators import login_required
from .forms import BillerForm


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
    form = BillerForm(request.POST)
    return render(request, 'index.html', {'form': form })


def biller(request):
    """
    :param request: receives the form in POST method
    :return: split data and start database search and call calculation
    """
    if request.method == "POST":
        form = BillerForm(request.POST)

    if form.is_valid():
        data = form.cleaned_data

    else:
        form = BillerForm()
        render(request, 'index.html', {'form': form})

    _subscriber = data['subscriber']
    _month = data['month']
    _year = data['year']

    if data['month'] in range(0, 13) and data['year'] in range(1900, 2099):
        _result = find_subscriber_month_year(subscriber=_subscriber, month=_month, year=_year)
    else:
        _result = find_subscriber(subscriber=_subscriber)

    return render(request, 'callslist.html', _result)


# @login_required
def find_subscriber(subscriber):
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

    else:
        endpoint = qs_data # cast for future implementations
        context = {'call_details': endpoint, 'subscriber': subscriber}

    return context
    # return render(request, 'callslist.html', context)


# @login_required
def find_subscriber_month_year(subscriber, month, year):
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
        endpoint = qs_data[1]
        context = {'info': endpoint, 'subscriber': subscriber}
    else:
        endpoint = qs_data  # cast for future implementations
        context = {'call_details': endpoint, 'subscriber': subscriber}

    return context
    ##return render(request, 'callslist.html', context)