from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)

    def __str__(self):
        return (self.item_name)