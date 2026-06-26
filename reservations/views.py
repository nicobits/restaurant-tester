from urllib.error import URLError
from urllib.request import Request, urlopen

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import MenuImportForm, ReservationForm
from .models import CustomerProfile, Reservation, Restaurant
from .repository import search_restaurants


def home(request):
    restaurants = Restaurant.objects.filter(is_active=True)[:12]
    neighborhoods = (
        Restaurant.objects.filter(is_active=True)
        .values_list("neighborhood", flat=True)
        .distinct()
        .order_by("neighborhood")
    )
    return render(
        request,
        "reservations/home.html",
        {"restaurants": restaurants, "neighborhoods": neighborhoods},
    )


def search(request):
    q = request.GET.get("q", "").strip()
    neighborhood = request.GET.get("neighborhood", "").strip()
    restaurants = search_restaurants(q=q, neighborhood=neighborhood)
    return render(
        request,
        "reservations/search_results.html",
        {"restaurants": restaurants, "q": q, "neighborhood": neighborhood},
    )


def restaurant_detail(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    upcoming = restaurant.reservations.exclude(status=Reservation.CANCELLED)[:5]
    return render(
        request,
        "reservations/restaurant_detail.html",
        {"restaurant": restaurant, "upcoming": upcoming},
    )


def reserve_table(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug, is_active=True)
    initial = {}

    if request.user.is_authenticated:
        initial = {
            "guest_name": request.user.get_full_name() or request.user.username,
            "guest_email": request.user.email,
        }

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.restaurant = restaurant
            if request.user.is_authenticated:
                reservation.guest = request.user
            reservation.save()
            messages.success(request, "Reservation confirmed.")
            return redirect("reservation_detail", reservation_id=reservation.id)
    else:
        form = ReservationForm(initial=initial)

    return render(
        request,
        "reservations/reservation_form.html",
        {"restaurant": restaurant, "form": form},
    )


def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, "reservations/reservation_detail.html", {"reservation": reservation})


@csrf_exempt
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method in ("GET", "POST"):
        reservation.status = Reservation.CANCELLED
        reservation.save(update_fields=["status", "updated_at"])
        messages.info(request, "Reservation cancelled.")

    return redirect("reservation_detail", reservation_id=reservation.id)


@login_required
def profile(request):
    profile, _ = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        for field_name, value in request.POST.items():
            if field_name != "csrfmiddlewaretoken" and hasattr(profile, field_name):
                setattr(profile, field_name, value)
        profile.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")

    return render(request, "reservations/profile.html", {"profile": profile})


@user_passes_test(lambda user: user.is_staff)
def staff_dashboard(request):
    reservations = Reservation.objects.select_related("restaurant", "guest")[:40]
    restaurants = Restaurant.objects.filter(is_active=True)
    return render(
        request,
        "reservations/staff_dashboard.html",
        {"reservations": reservations, "restaurants": restaurants},
    )


@user_passes_test(lambda user: user.is_staff)
def import_menu_preview(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    form = MenuImportForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        menu_url = form.cleaned_data["menu_url"]
        try:
            req = Request(menu_url, headers={"User-Agent": "RestaurantTester/1.0"})
            with urlopen(req, timeout=4) as response:
                preview = response.read(4096).decode("utf-8", errors="replace")
            restaurant.last_menu_fetch_url = menu_url
            restaurant.menu_import_preview = preview
            restaurant.save(update_fields=["last_menu_fetch_url", "menu_import_preview"])
            messages.success(request, "Menu preview imported.")
            return redirect("import_menu_preview", restaurant_id=restaurant.id)
        except (URLError, TimeoutError, ValueError) as exc:
            messages.error(request, f"Could not import menu preview: {exc}")

    return render(
        request,
        "reservations/import_menu_preview.html",
        {"restaurant": restaurant, "form": form},
    )
