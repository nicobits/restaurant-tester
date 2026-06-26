from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Reservation, Restaurant


class ReservationSmokeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="guest", email="guest@example.com", password="guestpass123"
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Bistro",
            slug="test-bistro",
            neighborhood="Chelsea",
            cuisine="Italian",
            address="100 W 20th St, New York, NY",
        )

    def test_home_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Bistro")

    def test_guest_can_create_reservation(self):
        self.client.login(username="guest", password="guestpass123")
        response = self.client.post(
            reverse("reserve_table", args=[self.restaurant.slug]),
            {
                "guest_name": "Avery Stone",
                "guest_email": "guest@example.com",
                "party_size": "2",
                "reservation_time": (timezone.now() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M"),
                "occasion_note": "Anniversary",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)
