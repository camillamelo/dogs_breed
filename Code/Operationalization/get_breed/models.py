from django.db import models

# Create your models here.

class Pictures(models.Model):
    id=models.AutoField(primary_key=True)
    address =  models.CharField(max_length=200, blank=False, null=False)
    real_breed = models.CharField(max_length=50, blank=True)
    classification = models.CharField(max_length=50, blank=True)
    class Meta:
        unique_together = ('address',)
