# models.py
from django.db import models

class Post(models.Model):
    title = models.TextField( blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # Add this field for categories

    def __str__(self):
        return self.title
