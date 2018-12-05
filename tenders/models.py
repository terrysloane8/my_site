from django.db import models
from django.utils import timezone

# Create your models here.


class Tender(models.Model):
    url = models.URLField()
    description = models.TextField()
    customer = models.CharField(max_length=255)
    bid_sum = models.FloatField()
    created = models.DateField()
    deadline = models.DateField()
    loaded = models.DateField(default=timezone.now)
    on_delete = models.BooleanField(default=False)


class Keyword(models.Model):
    word = models.CharField(max_length=255)
    chosen = models.BooleanField(default=True)
