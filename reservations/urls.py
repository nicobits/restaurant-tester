from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("restaurants/<slug:slug>/", views.restaurant_detail, name="restaurant_detail"),
    path("restaurants/<slug:slug>/reserve/", views.reserve_table, name="reserve_table"),
    path("reservations/<int:reservation_id>/", views.reservation_detail, name="reservation_detail"),
    path("reservations/<int:reservation_id>/cancel/", views.cancel_reservation, name="cancel_reservation"),
    path("profile/", views.profile, name="profile"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path(
        "staff/restaurants/<int:restaurant_id>/import-preview/",
        views.import_menu_preview,
        name="import_menu_preview",
    ),
]
