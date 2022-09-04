from django.db import models
from utils.models import City

# Create your models here.


class Cuisines(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=200)


class Restaurant(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    zomato_id = models.IntegerField()
    address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    image_url = models.URLField(null=True, blank=True, max_length=250)
    do_online_delivery = models.BooleanField(default=False)
    cuisines = models.ManyToManyField(Cuisines, related_name='cuisines')
