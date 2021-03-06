"""File for Model for Tasks"""
from django.db import models
from django.contrib.auth.models import User


class Tasks(models.Model):
    """Model for Tasks"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey("Categories", on_delete=models.CASCADE)
    create_date_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    completion_date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    