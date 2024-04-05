from django.test import TestCase
from django.db import models

# Create your tests here.

# class Auto(models.Model):
id = models.BigAutoField.get_internal_type(4)
print(id)