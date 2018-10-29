from datetime import timedelta
from decimal import *

from dateutil import parser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.utils.datetime_safe import datetime


class CallPair(models.Model):
    """ Temporary table for joining detailed call information
        Not implemented in REST API in version 1.0
        Can be further used directly from views.py to void parsing data
    """
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
        purge_subscriber = ''  # PEP8 declaration before try
        try:
            purge_subscriber = CallPair.objects.filter(source=subscriber)
            purge_subscriber.delete()
        except purge_subscriber.ObjectDoesNotExist:
            pass

        # avoid injection or large data inserted in subscriber var
        try:
            start = CallStartRecord.objects.filter(source=subscriber)
        except ObjectDoesNotExist:
            return [1, "Internal Error - please contact support: subscriber lenght: {0} - type {1}".format(
                len(subscriber), type(subscriber))]

        if start.count() == 0:
            return [2, "Subscriber was not found in database. Please check the subscriber number."]

        for call in start:
            cp = CallPair()
            try:
                pair = CallEndRecord.objects.get(call_id=call.call_id)
            except ObjectDoesNotExist:
                continue

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
                cp.closed_period_month = end_timestamp.month
                cp.closed_period_year = end_timestamp.year
                try:
                    cp.save()
                except IntegrityError:
                    return [1, "There was an Integrity Error during data saving. Please try again"]
        return [0, "Records were saved in the temp database"]


    def is_valid_period(self, start_timestamp, end_timestamp):
        try:
            # looking for a safe alternative to convert ISO-8601 datetime
            # "%Y-%m-%dT%H:%M:%S%Z") unsupported into python batteries prior py3.7
            # date string template from olist: 2016-02-29T14:00:00Z
            # converting both dates to naiwe datetime objects since format has no %Z just Z (zulu time)
            datetime.strptime(start_timestamp, "%Y-%m-%dT%H:%M:%SZ")
            start_timestamp = parser.parse(start_timestamp)  #
            is_valid_start_ts = True
        except ValueError:
            is_valid_start_ts = False
            return 1

        try:
            datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%SZ")
            end_timestamp = parser.parse(end_timestamp)
            is_valid_end_ts = True
        except ValueError:
            is_valid_end_ts = False
            return 1

        if is_valid_start_ts and is_valid_end_ts:
            if start_timestamp.replace(tzinfo=None) < end_timestamp.replace(tzinfo=None):
                return [start_timestamp, end_timestamp]
            else:
                return 1

    def get_interval_by_auto(self, subscriber):
        """ Search required subscriber number eg.: 99988526423 and return
            the last closed period call as list of Month and Year
        """

        call_pair_resume = self.get_call_pairs(subscriber=subscriber)

        if call_pair_resume is None:
            return [1, "No valid timestamp were found for this subscriber"]
        elif call_pair_resume[0] >= 1:
            return call_pair_resume  # return the error and description to view and frontend

        current_month = datetime.now().month
        current_year = datetime.now().year

        # excluding fields with invalid and empty data during the query search
        try:
            call_pair = CallPair.objects.filter(source=subscriber,
                                                dt_end__month__lt=current_month,
                                                dt_end__year__lte=current_year).latest('dt_end')
        except ObjectDoesNotExist:
            return [1, "No valid call records were found for this subscriber"]

        if call_pair.DoesNotExist is True:
            return [1, "There is no valid call pair for this subscriber and this period"]

        interval = self.get_interval_by_period(subscriber, call_pair.closed_period_year, call_pair.closed_period_month)

        return interval

    def get_interval_by_period(self, subscriber, year, month):
        """
        :param self: self-controlled
        :param subscriber: Subscriber number
        :param year: int 4 digits
        :param month: int 2 digits
        :return: dictionary with call details
        """

        call_details = []  # PEP8 specification
        call_matrix = dict()  # PEP8 specification

        # make sure subscriber exists
        call_pair_resume = self.get_call_pairs(subscriber=subscriber)
        if call_pair_resume[0] >= 1:
            return call_pair_resume  # return the error and description to view and frontend

        try:
            call_period = CallPair.objects.filter(source=subscriber, closed_period_month=month, closed_period_year=year)
        except ObjectDoesNotExist:
            return [3, "No matching results were found for this subscriber. Check data consistency"]

        # has no other method for counting. This can throw an error, if db is locked or with truncated data.
        # django documentation has no solution, and there is a bug fix open waiting for solution
        if call_period.count() == 0:
            return [4, "No matching results were found for this subscriber. Check data Consistency"]

        for call in call_period:
            call_matrix = self.call_calculator(call.dt_start, call.dt_end)

            call.price = call_matrix['call_price']
            call_matrix['destination'] = call.destination

            # save the price information in the @tempDataTable
            call.save()

            # return the dict call details into list like obj
            call_details.append(call_matrix)

        return call_details

    def call_calculator(self, timestamp_start, timestamp_end):
        """
        :param timestamp_start: datetime object
        :param timestamp_end: datetime object
        :return: dictionary containing: charge period, call price and senstive call information
                 for future implementations
        """
        # TODO: Research a better way to avoid using this schema

        normal_charge_period = [x for x in range(6, 22)]  # 6am to 22pm

        call_start_datetime = timestamp_start  # casting conventional var name to be used
        call_end_datetime = timestamp_end  # casting conventional var name

        # keeps detailed information from time DELTA between start and end call datetime obj
        call_total_duration = self.call_duration(call_start_datetime, call_end_datetime)

        # If call duration time between 6 and 22 hours / 0.09 cents per minute + 0.36 cents for call
        if (call_start_datetime.hour in normal_charge_period) & \
                (call_end_datetime.hour in normal_charge_period):

            # if call duration time between 6 and 22 hours of the same day
            if call_start_datetime.day == call_end_datetime.day:
                period_in_minutes = self.tm_delta(call_start_datetime, call_end_datetime)

                # casting for a better code reading
                feeder_resume = self.feeder(period_in_minutes, "normal", call_total_duration)
                return feeder_resume

            # else if call duration time exceeds a day
            else:
                end_charge_limit = call_start_datetime.replace(hour=22, minute=0, second=0)

                min_amount = end_charge_limit - call_start_datetime
                min_amount = min_amount / timedelta(minutes=1)

                start_charge_limit = call_end_datetime.replace(hour=6, minute=0, second=0)

                end_amount = call_end_datetime - start_charge_limit
                end_amount = end_amount / timedelta(minutes=1)
                amount = min_amount + end_amount

                # casting for a better code reading
                feeder_resume = self.feeder(amount, "normal", call_total_duration)

                return feeder_resume

        # If call_total_duration between reduced charge period / 22pm hour to 6am hour
        elif (call_start_datetime.hour not in normal_charge_period) & \
                (call_end_datetime.hour not in normal_charge_period):

            # keeps the total period in minutes to be evaluated by the feeder.
            period_in_minutes = self.tm_delta(call_start_datetime, call_end_datetime)

            # casting for a better code reading
            feeder_resume = self.feeder(period_in_minutes, "reduced_charge", call_total_duration)

            return feeder_resume

        # If call_total_duration starts between normal period and ends on reduced period / 22am hour before 6am hour
        elif (call_start_datetime.hour in normal_charge_period) & \
                (call_end_datetime.hour not in normal_charge_period):

            # fast way found to calculate feeder delta
            # TODO: Find a more elegant way to calculate this
            end_charge_limit = call_end_datetime.replace(hour=22, minute=0, second=0)
            period_in_minutes = self.tm_delta(call_start_datetime, end_charge_limit)

            return self.feeder(period_in_minutes, "partial", call_total_duration)

        # If call_total_duration starts after 22pm hour and ends after 6am hour
        elif (call_start_datetime.hour not in normal_charge_period) & \
                (call_end_datetime.hour in normal_charge_period):

            # change the time where the charging starts
            start_charge_limit = call_start_datetime.replace(hour=6, minute=0, second=0)
            period_in_minutes = self.tm_delta(start_charge_limit, call_end_datetime)

            # return detailed price information plus call duration
            return self.feeder(period_in_minutes, 'partial', call_total_duration)

    def call_duration(self, start, end):
        """
        :param start: datetime format
        :param end: datetime format
        :return: hh:mm:ss without microseconds when applicable
                 TODO: Further investigate DELTA weird behavior in POSIX systems
        """
        delta_diff = end - start

        _hours, rem = divmod(delta_diff.total_seconds(), 3600)
        _minutes, _seconds = divmod(rem, 60)

        # duplicated strips due bug prevention in POSIX
        duration = str(delta_diff).split('.')[0]
        duration_simplified = '{:02}h{:02}m{:02}s'.format(int(_hours), int(_minutes), int(_seconds))

        """ For future implementations a detailed dict, for plug and play.
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
            'call_duration': duration,  # %d days, %H:%M:%S
            'call_d_fmt': duration_simplified,
        }

    def tm_delta(self, start, end):
        diff = end - start
        diff = diff / timedelta(minutes=1)

        return diff

    def feeder(self, minutes, period_type, duration):
        """ Receives integer minutes, string type, duration timestamp return dict with
            detailed information about pricing
        """

        minutes = int(minutes)
        fixed_charge = float(0.36)  # standing charge for any call

        if period_type == "normal" or "partial":  # normal charge or partial charge
            minute_price = float(0.09)
        else:
            #  using float(0) since 0 was giving out weird behavior due POSIX-based architecture
            minute_price = float(0)  # no minute charge when whole call is out of 22 PM to 6 AM

        value = minutes * minute_price

        # a safe way to impose format this float in POSIX-based architecture when running in Win32 systems
        duration['call_price'] = float("{0:.2f}".format(value + fixed_charge))

        return duration
