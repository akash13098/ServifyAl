from django.db import models

class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.URLField(blank=True)

    def __str__(self):
        return self.name