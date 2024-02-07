"""List of imports"""

from django.db import models

# Create your models here.


class Article(models.Model):
    """Article model

    Args:
        models (Models): This model is for every article retrived on a website

    Returns:
        None: No return
    """

    Field1 = models.CharField(max_length=100)
    Field2 = models.CharField(max_length=100)
    Field3 = models.CharField(max_length=100)
    Field4 = models.CharField(max_length=100)
    Field5 = models.CharField(max_length=100)
    Field6 = models.CharField(max_length=100)
    Field7 = models.CharField(max_length=250)

    def __str__(self):
        return self.Field1 + " " + self.Field2
