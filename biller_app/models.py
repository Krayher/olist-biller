from django.db import models


class CallStartRecord(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField(null=True)
    call_id = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=50, null=True)
    destination = models.CharField(max_length=50, null=True)

    def __str(self):
        return 'SUBSCRIBER: {0} - CALL ID: {1}'.format(self.source, self.call_id)


class CallEndRecord(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=50, null=True)
    timestamp = models.DateTimeField()
    call_id = models.CharField(max_length=50, null=True)

    def __str(self):
        return 'CALL ID: {0}'.format(self.call_id)





# Create your models here.
