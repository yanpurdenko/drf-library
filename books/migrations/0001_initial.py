# Generated by Django 4.2 on 2023-04-20 16:07

import books.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("author", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "cover",
                    models.CharField(
                        choices=[("Hard", "Hard"), ("Soft", "Soft")], max_length=4
                    ),
                ),
                (
                    "inventory",
                    models.IntegerField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=4)),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=books.models.book_image_file_path
                    ),
                ),
                ("genres", models.ManyToManyField(blank=True, to="books.genre")),
            ],
            options={
                "ordering": ["title"],
            },
        ),
    ]
