from .category import Category
from django.db import models

class domain(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="domains")

    def __str__(self):
        return self.name
