from django.db import models


# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=255)
    learn_more_url = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    more_locations = models.CharField(max_length=255, blank=True)
    experience_level = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

