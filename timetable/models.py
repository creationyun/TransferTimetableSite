from django.db import models


class RequestedStation(models.Model):
    station_name = models.CharField(max_length=50)

    def __str__(self):
        return self.station_name
