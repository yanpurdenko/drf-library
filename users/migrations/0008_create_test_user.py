from django.db import migrations
from django.conf import settings
from django.contrib.auth import get_user_model


def create_test_user(apps, schema_editor):

    if not get_user_model().objects.filter(email=settings.TEST_USER_EMAIL).exists():
        get_user_model().objects.create_user(
            email=settings.TEST_USER_EMAIL,
            password=settings.TEST_USER_PASSWORD,
            is_superuser=True,
            is_staff=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0007_alter_user_id")
    ]

    operations = [
        migrations.RunPython(create_test_user, migrations.RunPython.noop),
    ]
