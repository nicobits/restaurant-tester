from django.contrib import admin

from .models import CustomerProfile, Reservation, Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "neighborhood", "cuisine", "rating", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "neighborhood", "cuisine")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "guest_name", "party_size", "reservation_time", "status")
    list_filter = ("status", "restaurant__neighborhood")
    search_fields = ("guest_name", "guest_email", "confirmation_code")


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "loyalty_tier", "phone", "is_concierge")
