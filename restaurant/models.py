from django.db import models
from utils.models import City, get_ext_id

# Create your models here.


class Cuisine(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name)


class Restaurant(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    zomato_id = models.IntegerField()
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    image_url = models.URLField(null=True, blank=True, max_length=250)
    do_online_delivery = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    cuisines = models.ManyToManyField(Cuisine, related_name='restaurants')

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name)
