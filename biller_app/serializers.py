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
                  'timestamp', #expected datetime ISOFORMAT with %Z military-tz
                  'call_id',
                  'source',
                  'destination')


class CallEndRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        """ Serializer for the END CALL record pair fields
        """
        model = CallEndRecord
        fields = ('id',
                  'type',
                  'timestamp', #expected datetime ISOFORMAT with %Z military-tz
                  'call_id')