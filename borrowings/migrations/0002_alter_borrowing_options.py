# Generated by Django 4.2 on 2023-05-07 09:46

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="borrowing",
            options={"ordering": ["borrow_date"]},
        ),
    ]
