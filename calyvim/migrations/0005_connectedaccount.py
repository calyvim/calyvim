# Generated by Django 5.0.3 on 2024-03-23 20:15

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calyvim", "0004_user_google_identity_uid"),
    ]

    operations = [
        migrations.CreateModel(
            name="ConnectedAccount",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "service",
                    models.CharField(
                        choices=[
                            ("google", "Google"),
                            ("microsoft", "Microsoft"),
                            ("zoom", "Zoom"),
                        ],
                        max_length=20,
                    ),
                ),
                ("access_token", models.CharField(max_length=255)),
                ("refresh_token", models.CharField(blank=True, max_length=255)),
                ("expiry_date", models.DateTimeField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="connected_accounts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "connected_accounts",
                "unique_together": {("user_id", "service")},
            },
        ),
    ]