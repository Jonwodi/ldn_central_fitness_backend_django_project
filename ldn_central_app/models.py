from django.db import models


class Gym(models.Model):
    name = models.CharField(max_length=255)
    gym_details = models.CharField(max_length=255, default="WHY PURE GYM")
    gym_link = models.URLField(max_length=255, default="https://www.puregym.com/")
    description = models.CharField(max_length=355)
    quality = models.CharField(max_length=355)
    access = models.CharField(max_length=355)
    network = models.CharField(max_length=355)
    contract = models.CharField(max_length=355)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
