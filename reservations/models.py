from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string


class Restaurant(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    neighborhood = models.CharField(max_length=80)
    cuisine = models.CharField(max_length=80)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, blank=True)
    price_level = models.PositiveSmallIntegerField(default=2)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.2)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    last_menu_fetch_url = models.URLField(blank=True)
    menu_import_preview = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["neighborhood", "name"]

    def __str__(self):
        return self.name


class Reservation(models.Model):
    REQUESTED = "requested"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (REQUESTED, "Requested"),
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="reservations")
    guest = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reservations",
        null=True,
        blank=True,
    )
    guest_name = models.CharField(max_length=120)
    guest_email = models.EmailField()
    party_size = models.PositiveSmallIntegerField()
    reservation_time = models.DateTimeField(default=timezone.now)
    occasion_note = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=16, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-reservation_time"]

    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            self.confirmation_code = get_random_string(12).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest_name} at {self.restaurant.name}"


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True)
    loyalty_tier = models.CharField(max_length=40, default="Silver")
    account_credit = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_concierge = models.BooleanField(default=False)
    dining_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.email or self.user.username} profile"
