# Generated by Django 4.2 on 2023-04-24 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("books", "0003_alter_book_inventory"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Borrowing",
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
                ("borrow_date", models.DateField(auto_now=True)),
                ("expected_return_date", models.DateField()),
                ("actual_return_date", models.DateField(blank=True, null=True)),
                (
                    "book_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="books.book"
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(("expected_return_date__gt", models.F("borrow_date"))),
                name="check_expected_return_date",
            ),
        ),
        migrations.AddConstraint(
            model_name="borrowing",
            constraint=models.CheckConstraint(
                check=models.Q(
                    models.Q(
                        ("actual_return_date__isnull", True),
                        ("actual_return_date__gte", models.F("borrow_date")),
                        _connector="OR",
                    )
                ),
                name="check_actual_return_date",
            ),
        ),
    ]
