from django.db import models
import random

# Create your models here.


def get_ext_id():
    return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') for _ in range(10))


class Country(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name)


class City(models.Model):
    ext_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    city_id = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s" % (self.name)
