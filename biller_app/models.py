from django.db import models
from django.utils.datetime_safe import datetime
from datetime import timedelta


class CallStartRecord(models.Model):
    """Receiver most in CharField format to avoid data discrepancies
       id models is set as not auto positive integer, allowing
       consumer to point its value.
    """
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    call_id = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    destination = models.CharField(max_length=50, null=True, blank=True)

    def __str(self):
        return 'SUBSCRIBER: {0} - CALL ID: {1}'.format(self.source, self.call_id)

    def checkconsistency(self):
        pass

    def closedperiod(self, subscriber, year, month):

        call_list = []

        queryset = self.objects.filter(source=subscriber,
                                       timestamp__month=month,
                                       timestamp__year=year)

        for call_start in queryset:
            call_end = CallEndRecord.objects.get(
                call_id=call_start.call_id)

            if call_end.timestamp.month == month:
                call_details = self.call_calculator(call_start.timestamp,
                                                    call_end.timestamp)

                call_details['destination'] = call_start.destination
                call_list.append(call_details)

        return dict({'call_details': call_list})


class CallEndRecord(models.Model):
    """Receiver most in CharField format to avoid data discrepancies
       id models is set as not auto positive integer, allowing
       consumer to point its value.
    """
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField(null=True, blank=True)
    call_id = models.CharField(max_length=50, null=True)

    def __str(self):
        return 'CALL ID: {0}'.format(self.call_id)


class QueryFilters():
    """Useful methods for filtering data accordingly"""

    @staticmethod
    def getsubscriberlatestperiod(self, subscriber):
        """
            To measure the latest closed period we need to get the END CALL RECORD timestamp
            instead of START CALL RECORD timestamp, due calls starting between last days of a month
            and being finished in the first day of a new one... It's showtime()
        """

        call_start_queryset = CallStartRecord.objects.filter(
            source=subscriber).latest('timestamp')

        call_end_queryset = CallEndRecord.objects.get(
            call_id=call_start_queryset.call_id)

        if call_end_queryset.timestamp.year <= datetime.now().year:
            if call_end_queryset.timestamp.month != datetime.now().month:
                return [call_end_queryset.timestamp.year, call_end_queryset.timestamp.month]
            else:
                return 1

    @staticmethod
    def call_pair(self, subscriber, year, month):
        call_start_recordset = CallStartRecord.objects.filter(source=subscriber,
                                                              timestamp__month=month,
                                                              timestamp__year=year)

        for call_start in call_start_recordset:
            call_end = CallEndRecord.objects.get(
                call_id=call_start.call_id)

            if call_end.timestamp.month == month and call_end.timestamp.year == year:
                pass

