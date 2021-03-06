"""Tasktag model Module"""
from django.db import models

class TaskTags(models.Model):
    """Tasktag database model"""
    task = models.ForeignKey("Tasks", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tags", on_delete=models.CASCADE)