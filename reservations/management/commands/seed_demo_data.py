from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from reservations.models import CustomerProfile, Reservation, Restaurant


class Command(BaseCommand):
    help = "Seed local demo restaurants, users, and reservations."

    def handle(self, *args, **options):
        User = get_user_model()

        guest, _ = User.objects.get_or_create(
            username="guest",
            defaults={"email": "guest@example.com", "first_name": "Avery", "last_name": "Stone"},
        )
        guest.set_password("guestpass123")
        guest.email = "guest@example.com"
        guest.save()

        host, _ = User.objects.get_or_create(
            username="host",
            defaults={"email": "host@example.com", "first_name": "Maya", "last_name": "Patel"},
        )
        host.set_password("staffpass123")
        host.email = "host@example.com"
        host.is_staff = True
        host.save()

        CustomerProfile.objects.update_or_create(
            user=guest,
            defaults={"phone": "212-555-0134", "loyalty_tier": "Gold", "dining_notes": "Prefers booths."},
        )
        CustomerProfile.objects.update_or_create(
            user=host,
            defaults={"phone": "212-555-0199", "loyalty_tier": "Staff", "is_concierge": True},
        )

        restaurants = [
            {
                "name": "Canal Hearth",
                "slug": "canal-hearth",
                "neighborhood": "SoHo",
                "cuisine": "New American",
                "address": "181 Grand St, New York, NY",
                "price_level": 3,
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1559339352-11d035aa65de",
                "description": "Seasonal downtown dining with a wood-fired menu and late bar seats.",
            },
            {
                "name": "Juniper Room",
                "slug": "juniper-room",
                "neighborhood": "West Village",
                "cuisine": "French",
                "address": "42 Perry St, New York, NY",
                "price_level": 4,
                "rating": 4.8,
                "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4",
                "description": "Quiet bistro with a compact wine list and two private alcove tables.",
            },
            {
                "name": "Mott Street Noodle",
                "slug": "mott-street-noodle",
                "neighborhood": "Chinatown",
                "cuisine": "Cantonese",
                "address": "15 Mott St, New York, NY",
                "price_level": 2,
                "rating": 4.5,
                "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9",
                "description": "Fast-moving dining room known for roast meats, noodles, and large tables.",
            },
            {
                "name": "Atlantic Oyster Bar",
                "slug": "atlantic-oyster-bar",
                "neighborhood": "Brooklyn Heights",
                "cuisine": "Seafood",
                "address": "88 Atlantic Ave, Brooklyn, NY",
                "price_level": 3,
                "rating": 4.4,
                "image_url": "https://images.unsplash.com/photo-1551218808-94e220e084d2",
                "description": "Raw bar, grilled fish, and patio seating near the waterfront.",
            },
            {
                "name": "Lenox Supper Club",
                "slug": "lenox-supper-club",
                "neighborhood": "Harlem",
                "cuisine": "Southern",
                "address": "230 Lenox Ave, New York, NY",
                "price_level": 3,
                "rating": 4.7,
                "image_url": "https://images.unsplash.com/photo-1528605248644-14dd04022da1",
                "description": "Supper club with live piano, fixed-price menus, and room for celebrations.",
            },
            {
                "name": "Jackson Heights Masala",
                "slug": "jackson-heights-masala",
                "neighborhood": "Jackson Heights",
                "cuisine": "Indian",
                "address": "74-12 37th Rd, Queens, NY",
                "price_level": 2,
                "rating": 4.6,
                "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe",
                "description": "North Indian cooking, thalis, and family-style reservations.",
            },
        ]

        created = []
        for item in restaurants:
            restaurant, _ = Restaurant.objects.update_or_create(slug=item["slug"], defaults=item)
            created.append(restaurant)

        Reservation.objects.get_or_create(
            restaurant=created[0],
            guest=guest,
            guest_email="guest@example.com",
            guest_name="Avery Stone",
            party_size=2,
            reservation_time=timezone.now() + timedelta(days=2, hours=2),
            defaults={"occasion_note": "Window table if possible.", "status": Reservation.CONFIRMED},
        )
        Reservation.objects.get_or_create(
            restaurant=created[1],
            guest_email="casey@example.com",
            guest_name="Casey Morgan",
            party_size=4,
            reservation_time=timezone.now() + timedelta(days=4, hours=1),
            defaults={"occasion_note": "Birthday dinner, prefers low lighting.", "status": Reservation.CONFIRMED},
        )

        self.stdout.write(self.style.SUCCESS("Seeded demo users, restaurants, and reservations."))
