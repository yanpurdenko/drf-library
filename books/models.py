import os
import uuid

from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


def book_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/books/", filename)


class Book(models.Model):
    COVER_CHOICES = (
        ("Hard", "Hard"),
        ("Soft", "Soft"),
    )

    title = models.CharField(max_length=255, unique=True)
    author = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(default=1)
    daily_fee = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(null=True, upload_to=book_image_file_path)

    @property
    def price_display(self) -> str:
        return "$%s" % self.daily_fee

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} - {self.author} (Inventory: {self.inventory})"
