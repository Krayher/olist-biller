from django.test import TestCase
from .models import  CallStartRecord, CallEndRecord, CallPair


class CallStartTest(TestCase):
    def setUp(self):
        CallStartRecord.objects.create(call_id=90009, source=99999999999, timestamp='2016-02-29T12:00:00Z',
                                       destination=99111111111)

        CallStartRecord.objects.create ( call_id=90008, source=99999999998, timestamp='2017-03-30T09:20:20Z',
                                         destination=99111111111)

    def testcall(self):
        dummie1 = CallStartRecord.objects.get(call_id=90009)
        dummie2 = CallStartRecord.objects.get ( call_id=90008)

        self.assertEqual(dummie1.timestamp)
        self.assertEqual(dummie2.destination)


class CallEndTest(TestCase):
    def setUp(self):
        CallEndRecord.objects.create(call_id=90009, source=99999999999, timestamp='2016-02-29T21:57:00Z')
        CallEndRecord.objects.create ( call_id=90008, source=99999999998, timestamp='2017-03-31T09:07:10Z')

    def testcall(self):
        dummie1 = CallEndRecord.objects.get(call_id=90009)
        dummie2 = CallEndRecord.objects.get(call_id=90008)

        self.assertEqual(dummie1.timestamp)
        self.assertEqual(dummie2.timestamp)


class CallPair(TestCase):
    def setUp(self):
        CallPair.objects.create(source=99999999999, timestamp='2016-02-29T21:57:00Z', price="57.10")
        CallPair.objects.create ( source=99999999998, timestamp='2016-02-29T21:58:00Z', price="58.10" )

    def testcall(self):
        dummie1 = CallPair.objects.get(source=99999999999)
        dummie2 = CallEndRecord.objects.get(source=99999999998)

        self.assertEqual(dummie1.price)
        self.assertEqual(dummie2.price)
