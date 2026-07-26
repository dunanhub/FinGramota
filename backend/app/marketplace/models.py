from django.db import models
from django.utils.text import slugify


class Bank(models.Model):
    name = models.CharField(max_length=255, unique=True)
    official_url = models.URLField(max_length=500)

    class Meta:
        ordering = ['name']

    @property
    def slug(self):
        return slugify(self.name)

    def __str__(self):
        return self.name
