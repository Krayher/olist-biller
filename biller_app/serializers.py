from rest_framework import serializers
from .models import CallStartRecord, CallEndRecord


class CallStartRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        """ Using the predefined template for REST API by Django REST API
            with the fields provieded by the contest README
        """
        model = CallStartRecord
        fields = ('id',
                  'type',
                  'timestamp',
                  'call_id',
                  'source',
                  'destination')
