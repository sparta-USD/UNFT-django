from django.db import models

# Create your models here.
class Unft(models.Model):
    title = models.CharField(max_length=100)
    