from django.conf import settings
from django.db import models
# Create your models here.

class ProductModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )
    title = models.TextField()
    price = models.FloatField()
    description = models.TextField(blank=True)  # Asegúrate de que esto esté presente
    seller = models.CharField(max_length=255, blank=True)
    color = models.CharField(max_length=50, blank=True)
    product_dimensions = models.CharField(max_length=100, blank=True)
