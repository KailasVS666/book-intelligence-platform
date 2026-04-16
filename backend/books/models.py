from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    rating = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title