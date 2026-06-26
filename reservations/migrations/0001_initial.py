import decimal

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Restaurant",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("neighborhood", models.CharField(max_length=80)),
                ("cuisine", models.CharField(max_length=80)),
                ("address", models.CharField(max_length=200)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("price_level", models.PositiveSmallIntegerField(default=2)),
                ("rating", models.DecimalField(decimal_places=1, default=4.2, max_digits=3)),
                ("image_url", models.URLField(blank=True)),
                ("description", models.TextField(blank=True)),
                ("last_menu_fetch_url", models.URLField(blank=True)),
                ("menu_import_preview", models.TextField(blank=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["neighborhood", "name"],
            },
        ),
        migrations.CreateModel(
            name="CustomerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("loyalty_tier", models.CharField(default="Silver", max_length=40)),
                ("account_credit", models.DecimalField(decimal_places=2, default=decimal.Decimal("0"), max_digits=8)),
                ("is_concierge", models.BooleanField(default=False)),
                ("dining_notes", models.TextField(blank=True)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("guest_name", models.CharField(max_length=120)),
                ("guest_email", models.EmailField(max_length=254)),
                ("party_size", models.PositiveSmallIntegerField()),
                ("reservation_time", models.DateTimeField(default=django.utils.timezone.now)),
                ("occasion_note", models.TextField(blank=True)),
                ("confirmation_code", models.CharField(blank=True, max_length=16, unique=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("requested", "Requested"),
                            ("confirmed", "Confirmed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="confirmed",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "guest",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reservations",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reservations",
                        to="reservations.restaurant",
                    ),
                ),
            ],
            options={
                "ordering": ["-reservation_time"],
            },
        ),
    ]
