from django.contrib import admin
from restaurant.models import Restaurant, Cuisines

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Cuisines)
