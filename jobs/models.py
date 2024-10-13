from django.db import models


# Create your models here.
class Job(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('stashed', 'Stashed'),
    )

    class Meta:
        db_table = "google_job_table"

    title = models.CharField(max_length=255)
    learn_more_url = models.TextField()
    location = models.CharField(max_length=255, blank=True)
    more_locations = models.CharField(max_length=255, blank=True)
    experience_level = models.CharField(max_length=255, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
    )
    
    def __str__(self):
        return self.title

