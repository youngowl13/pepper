from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.models import get_ext_id
from users.manager import UserManager

# Create your models here.


class Role(models.Model):

    MANAGER = 0
    SALES = 1
    INVENTORY = 2
    CUSTOMER = 3
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (SALES, 'Sales'),
        (INVENTORY, 'Inventory'),
        (CUSTOMER, 'Customer')
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractUser):
    ext_id = models.CharField(max_length=10)
    email = models.CharField(max_length=255, unique=True)
    roles = models.ManyToManyField(Role)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        while not self.ext_id:
            new_id = get_ext_id()
            if not type(self).objects.filter(ext_id=new_id).exists():
                self.ext_id = new_id
        super().save(*args, **kwargs)
