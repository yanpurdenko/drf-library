# Generated by Django 4.2 on 2023-05-07 09:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("c28878e1-9e22-467c-a84a-4921a6a0d123"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]