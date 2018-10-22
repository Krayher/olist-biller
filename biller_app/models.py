from django.db import models, IntegrityError
from django.utils.datetime_safe import datetime
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist
import time


class CallPair(models.Model):
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    call_id = models.CharField(max_length=10, unique=True)
    dt_start = models.DateTimeField()
    dt_end = models.DateTimeField()

    # Optional fields to be implemented in a future version
    duration = models.CharField(max_length=50)
    closed_period_month = models.CharField(max_length=5)
    closed_period_year = models.CharField(max_length=5)
    price = models.CharField(max_length=10)
    total_price = models.CharField(max_length=10)

    def __str__(self):
        return str(self.source + " " + self.call_id)



class CallStartRecord(models.Model):
    """Receiver most in CharField format to avoid data discrepancies
       id models is set as not auto positive integer, allowing
       consumer to point its value.
    """
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=50, null=True)
    timestamp = models.CharField(max_length=50, null=True, blank=True)
    call_id = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    destination = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return 'SUBSCRIBER: {0} - CALL ID: {1}'.format(self.source, self.call_id)

    
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

                # creating the destination filed in the fresh returned dict
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
    timestamp = models.CharField(max_length=50, null=True, blank=True)
    call_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return 'CALL ID: {0}'.format(self.call_id)


class QueryFilters:
    """Useful methods for filtering data accordingly"""

    def __init__(self):
        pass


    def get_call_pairs(self, subscriber):
        """

        :param subscriber: The phone number eg. 99988526423
        :return: reunite each call detail in a table to make life easier
        """

        purge_subscriber = CallPair.objects.filter(source=subscriber)
        purge_subscriber.delete()

        try:
            start = CallStartRecord.objects.filter(source=subscriber)
        except ObjectDoesNotExist:
            return 1

        for call in start:
            cp = CallPair()
            try:
                pair = CallEndRecord.objects.get(call_id=call.call_id)
            except ObjectDoesNotExist:
                pass

            datetime_validation = self.is_valid_period(call.timestamp, pair.timestamp)
            if datetime_validation == 1:
                continue
            else:
                start_timestamp = datetime_validation[0]
                end_timestamp = datetime_validation[1]

                cp.source = call.source
                cp.destination = call.destination
                cp.call_id = call.call_id
                cp.dt_start = start_timestamp
                cp.dt_end = end_timestamp
                cp.closed_period_month =  end_timestamp.month
                cp.closed_period_year = end_timestamp.year
                try:
                    cp.save()
                except IntegrityError:
                    continue


    def is_valid_period(self, start_timestamp, end_timestamp):
        try:
            start_timestamp = parse_datetime(start_timestamp) # safe alternative to datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%S%Z") unsupported on python batteries
            is_valid_start_ts = True
        except ValueError:
            is_valid_start_ts = False
            pass

        try:
            end_timestamp = parse_datetime(end_timestamp) # datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S%Z")
            is_valid_end_ts = True
        except ValueError:
            is_valid_end_ts = False
            pass

        if is_valid_start_ts and is_valid_end_ts:
            if start_timestamp.replace(tzinfo=None) < end_timestamp.replace(tzinfo=None):
                return [start_timestamp.replace(tzinfo=None), end_timestamp.replace(tzinfo=None)]
            else:
                return 1




    def get_interval_by_subscriber(self, subscriber):
        """ Search required subscriber number eg.: 99988526423 and return
            the last closed period call as list of Month and Year
        """

        self.get_call_pairs(subscriber=subscriber)

        current_month = datetime.now().month
        current_year = datetime.now().year
        closed_period = []

        # Django plus size framework give us a validation during the filtering
        # excluding fields with invalid and empty data during the query search
        try:
            call_start_queryset = CallStartRecord.objects.filter(source=subscriber,
                                                         timestamp__month__lt=current_month,
                                                         timestamp__year__lte=current_year).latest('timestamp')
        except ObjectDoesNotExist:
            return 1 #  Return code for call records not found

        latest_call_id = call_start_queryset.call_id

        try:
            call_end_queryset = CallEndRecord.objects.get(call_id=latest_call_id,
                                                          timestamp__month__gte=call_start_queryset.timestamp.month,
                                                          timestamp__year__gte=call_start_queryset.timestamp.year)
        except ObjectDoesNotExist:
            return 2 #  Return code for call records not found

        if call_end_queryset.timestamp.month < current_month and call_end_queryset.timestamp.year <= current_year:
            closed_period.append(call_end_queryset.timestamp.month)
            closed_period.append(call_end_queryset.timestamp.year)

        return closed_period

    
    def get_by_full_call_list(self, subscriber, year, month):
        """
        :param self: Iluminate yourself
        :param subscriber: Subscriber number
        :param year: int 4 digits
        :param month: int 2 digits
        :return: dictionary with call details
        """

        call_details = []
        call_matrix = dict()

        # make sure that closed period informed is in the same month when calls has ended.

        try:
            call_start_recordset = CallStartRecord.objects.filter(source=subscriber,
                                                                  timestamp__month=month,
                                                                  timestamp__year=year)
        except ObjectDoesNotExist:
            return 1 # Return code for missing subscriber and its filters

        if len(call_start_recordset) == 0:
            try:
                # This occurs when a call starts 31st and ends up in the next day 1 from next month
                call_start_recordset = CallStartRecord.objects.filter(source=subscriber,
                                                                      timestamp__month__lte=month,
                                                                      timestamp__year__lte=year)
            except ObjectDoesNotExist:
                return 1  # If something goes wrong during filtering !!! ALERT !!!

        if len(call_start_recordset) == 0:
            return 1

        for call_start in call_start_recordset:
            call_end = CallEndRecord.objects.get(
                call_id=call_start.call_id)

            if call_end.timestamp.month == month and call_end.timestamp.year == year:
                call_matrix = self.call_calculator(call_start.timestamp, call_end.timestamp)
                call_matrix['destination'] = call_start.destination
                call_details.append(call_matrix)

        if call_matrix:
            return call_details
        else:
            return 1

    
    def call_calculator(self, timestamp_start, timestamp_end):

        normal_charge = [x for x in range(6, 22)]

        call_start = timestamp_start  # conventional var name to be used
        call_end = timestamp_end  # conventional var name

        call_total_duration = self.call_duration(
            call_start, call_end)

        # If call duration time between 6 and 22 hours / 5 cents per minute + 10 cents for call
        if (call_start.hour in normal_charge) & \
                (call_end.hour in normal_charge):

            # if call duration time between 6 and 22 hours of the same day
            if call_start.day == call_end.day:
                period_in_minutes = self.tm_delta(call_start, call_end)

                return self.taxing(period_in_minutes, "normal", call_total_duration)

            # else if call duration time exceeds a day
            # TODO: find a time to research a better way to avoid this messy code
            else:
                end_charge_limit = call_start.replace(hour=22,
                                                      minute=0)

                min_amount = end_charge_limit - call_start
                min_amount = min_amount / timedelta(minutes=1)

                start_charge_limit = call_end.replace(hour=6,
                                                      minute=0)

                end_amount = call_end - start_charge_limit
                end_amount = end_amount / timedelta(minutes=1)

                amount = min_amount + end_amount

                return self.taxing(amount, "normal", call_total_duration)

        # If call_total_duration between reduced charge period / 22pm hour to 6am hour
        elif (call_start.hour not in normal_charge) & \
                (call_end.hour not in normal_charge):

            period_in_minutes = self.tm_delta(call_start,
                                              call_end)

            return self.taxing(period_in_minutes, "reduced_charge", call_total_duration)

        # If call_total_duration starts between normal period and ends on reduced period / 22am hour before 6am hour
        elif (call_start.hour in normal_charge) & \
                (call_end.hour not in normal_charge):

            end_charge_limit = call_end.replace(hour=22,
                                                minute=0)

            period_in_minutes = self.tm_delta(call_start,
                                              end_charge_limit)

            return self.taxing(period_in_minutes,
                               "partial",
                               call_total_duration)

        # If call_total_duration starts after 22pm hour and ends after 6am hour
        elif (call_start.hour not in normal_charge) & \
                (call_end.hour in normal_charge):

            start_charge_limit = call_start.replace(hour=6,
                                                    minute=0)

            period_in_minutes = self.tm_delta(start_charge_limit,
                                              call_end)

            # return detailed price information plus call duration
            return self.taxing(period_in_minutes,
                               'partial',
                               call_total_duration)

    
    def call_duration(self, start, end):
        delta_diff = end - start
        duration = str(delta_diff).split('.')[0]

        """ The initial problema doesn't require such detailed information, however
            for future detailed information it's already done, just plug and play.
        """
        return {
            'start_date': datetime.strftime(start, '%Y/%m/%d'),
            'start_time': datetime.strftime(start, '%H:%M:%S'),
            'start_day': start.day,
            'start_mon': start.month,
            'start_year': start.year,
            'start_hour': start.hour,
            'start_min': start.minute,
            'start_sec': start.second,
            'end_date': datetime.strftime(end, '%Y/%m/%d'),
            'end_time': datetime.strftime(end, '%H:%M:%S'),
            'end_day': end.day,
            'end_mon': end.month,
            'end_year': end.year,
            'end_hour': end.hour,
            'end_min': end.minute,
            'end_sec': end.second,
            'call_duration': duration,  # %H;%M:%S
            'call_duration_deltafmt': str(delta_diff),  # %D days %H:%M:%S
        }
    
    def tm_delta(self, start, end):
        diff = end - start
        diff = diff / timedelta(minutes=1)

        return diff

    def taxing(self, minutes, type, duration):
        minutes = int(minutes)
        fixed_charge = float(0.11)
        if type == "normal" or "partial":
            minute_price = float(0.05)
        else:
            minute_price = float(0)

        value = minutes * minute_price
        duration['call_price'] = float(value + fixed_charge)

        return duration

