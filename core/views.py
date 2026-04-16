from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AdminBookingStatusForm,
    AdminServiceForm,
    AdminStylistUpdateForm,
    BookingForm,
    CustomerRegistrationForm,
    StylistProfileForm,
)
from .models import Booking, Service, StylistProfile


def require_admin(request):
    # Reuse this guard across the custom admin views.
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to view the admin area.")
        return redirect("home")
    return None


def home(request):
    services = Service.objects.all()[:6]
    stylists = StylistProfile.objects.filter(is_available=True)[:3]
    context = {
        "services": services,
        "stylists": stylists,
        "booking_count": Booking.objects.count(),
    }
    return render(request, "core/home.html", context)


def service_list(request):
    services = Service.objects.all()
    return render(request, "core/services.html", {"services": services})


def stylist_list(request):
    location_query = request.GET.get("location", "").strip()
    # Only available stylists are shown to keep booking choices simple.
    stylists = StylistProfile.objects.filter(is_available=True)

    if location_query:
        stylists = stylists.filter(location__icontains=location_query)

    context = {
        "stylists": stylists,
        "location_query": location_query,
    }
    return render(request, "core/stylists.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("home")
    else:
        form = CustomerRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def stylist_register(request):
    # A stylist can create a profile once and then edit the same record later.
    existing_profile = StylistProfile.objects.filter(user=request.user).first()
    is_editing = existing_profile is not None

    if request.method == "POST":
        form = StylistProfileForm(
            request.POST, request.FILES, instance=existing_profile
        )
        if form.is_valid():
            stylist_profile = form.save(commit=False)
            stylist_profile.user = request.user
            stylist_profile.save()
            if is_editing:
                messages.success(request, "Your stylist profile was updated successfully.")
            else:
                messages.success(request, "Your stylist profile has been created.")
            return redirect("stylists")
    else:
        form = StylistProfileForm(instance=existing_profile)

    context = {
        "form": form,
        "is_editing": is_editing,
    }
    return render(request, "core/stylist_register.html", context)


@login_required
def book_service(request):
    # Query parameters let users prefill the form from service and stylist listings.
    initial_data = {}
    service_id = request.GET.get("service")
    stylist_id = request.GET.get("stylist")

    if service_id:
        service = get_object_or_404(Service, id=service_id)
        initial_data["service"] = service

    if stylist_id:
        stylist = get_object_or_404(StylistProfile, id=stylist_id, is_available=True)
        initial_data["stylist"] = stylist

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            # Attach the logged-in customer instead of exposing that field in the form.
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.save()
            messages.success(request, "Your booking was submitted successfully.")
            return redirect("booking_list")
    else:
        form = BookingForm(initial=initial_data)

    return render(request, "core/book_service.html", {"form": form})


@login_required
def booking_list(request):
    # Superuser can review every booking, while customers see only their own.
    if request.user.is_superuser:
        bookings = Booking.objects.select_related(
            "customer", "stylist", "service"
        ).all()
    else:
        bookings = Booking.objects.select_related(
            "customer", "stylist", "service"
        ).filter(customer=request.user)

    return render(request, "core/bookings.html", {"bookings": bookings})


@login_required
def admin_dashboard(request):
    denied = require_admin(request)
    if denied:
        return denied

    # Pull related records once so the dashboard tables stay efficient.
    bookings = Booking.objects.select_related("customer", "stylist", "service")
    recent_bookings = bookings.order_by("-created_at")[:5]
    # Build quick lookup counts for each booking status.
    status_counts = {
        item["status"]: item["total"]
        for item in bookings.values("status").annotate(total=Count("id"))
    }

    context = {
        "total_bookings": bookings.count(),
        "total_services": Service.objects.count(),
        "total_stylists": StylistProfile.objects.count(),
        "available_stylists": StylistProfile.objects.filter(is_available=True).count(),
        "pending_bookings": status_counts.get(Booking.STATUS_PENDING, 0),
        "confirmed_bookings": status_counts.get(Booking.STATUS_CONFIRMED, 0),
        "completed_bookings": status_counts.get(Booking.STATUS_COMPLETED, 0),
        "recent_bookings": recent_bookings,
        "active_admin_tab": "dashboard",
    }
    return render(request, "core/admin/dashboard.html", context)


@login_required
def admin_bookings(request):
    denied = require_admin(request)
    if denied:
        return denied

    if request.method == "POST":
        booking = get_object_or_404(Booking, id=request.POST.get("booking_id"))
        form = AdminBookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking status updated successfully.")
            return redirect("admin_bookings")

    bookings = Booking.objects.select_related("customer", "stylist", "service").all()
    context = {
        "bookings": bookings,
        "status_choices": Booking.STATUS_CHOICES,
        "active_admin_tab": "bookings",
    }
    return render(request, "core/admin/bookings.html", context)


@login_required
def admin_services(request):
    denied = require_admin(request)
    if denied:
        return denied

    # The same form handles both creating and editing services.
    editing_service = None
    service_id = request.GET.get("edit")
    if service_id:
        editing_service = get_object_or_404(Service, id=service_id)

    if request.method == "POST":
        editing_service = None
        post_service_id = request.POST.get("service_id")
        if post_service_id:
            editing_service = get_object_or_404(Service, id=post_service_id)

        form = AdminServiceForm(request.POST, request.FILES, instance=editing_service)
        if form.is_valid():
            form.save()
            if editing_service:
                messages.success(request, "Service updated successfully.")
            else:
                messages.success(request, "Service created successfully.")
            return redirect("admin_services")
    else:
        form = AdminServiceForm(instance=editing_service)

    context = {
        "form": form,
        "services": Service.objects.all(),
        "editing_service": editing_service,
        "active_admin_tab": "services",
    }
    return render(request, "core/admin/services.html", context)


@login_required
def admin_stylists(request):
    denied = require_admin(request)
    if denied:
        return denied

    if request.method == "POST":
        stylist = get_object_or_404(StylistProfile, id=request.POST.get("stylist_id"))
        form = AdminStylistUpdateForm(request.POST, instance=stylist)
        if form.is_valid():
            form.save()
            messages.success(request, "Stylist profile updated successfully.")
            return redirect("admin_stylists")

    stylists = StylistProfile.objects.select_related("user").all()
    context = {
        "stylists": stylists,
        "active_admin_tab": "stylists",
    }
    return render(request, "core/admin/stylists.html", context)
