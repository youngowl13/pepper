from django.db import models
from utils.models import get_ext_id
from restaurant.models import Restaurant


class Order(models.Model):
    ext_id = models.CharField(max_length=10)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    product = models.JSONField()
    created = models.DateTimeField(auto_now_add=True, blank=True)
    total_price = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
