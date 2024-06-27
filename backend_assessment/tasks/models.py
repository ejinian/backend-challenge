from django.contrib.auth.models import User
from django.db import models

class Label(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'owner')
        verbose_name_plural = 'Labels'

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, blank=True)

    def __str__(self):
        return self.title