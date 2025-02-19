from django.db import models

class LostItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="lost_items/")
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_lost = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FoundItem(models.Model):
    image = models.ImageField(upload_to="found_items/")
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    date_found = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Found at {self.location}"
