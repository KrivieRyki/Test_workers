from django.db import models


class DriverLog(models.Model):
    STATUS_CHOICES = (
        ('working', 'Working'),
        ('resting', 'Resting'),
        ('off', 'Off'),
    )
    company_id = models.IntegerField()
    create_date = models.DateTimeField()
    driver_id = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return f"DriverLog {self.id}"
