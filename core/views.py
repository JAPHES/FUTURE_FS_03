from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm, CustomerRegistrationForm, StylistProfileForm
from .models import Booking, Service, StylistProfile


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
    existing_profile = StylistProfile.objects.filter(user=request.user).first()
    if existing_profile:
        messages.info(request, "You already have a stylist profile.")
        return redirect("stylists")

    if request.method == "POST":
        form = StylistProfileForm(request.POST, request.FILES)
        if form.is_valid():
            stylist_profile = form.save(commit=False)
            stylist_profile.user = request.user
            stylist_profile.save()
            messages.success(request, "Your stylist profile has been created.")
            return redirect("stylists")
    else:
        form = StylistProfileForm()

    return render(request, "core/stylist_register.html", {"form": form})


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
    # Staff users can review every booking, while customers see only their own.
    if request.user.is_staff:
        bookings = Booking.objects.select_related(
            "customer", "stylist", "service"
        ).all()
    else:
        bookings = Booking.objects.select_related(
            "customer", "stylist", "service"
        ).filter(customer=request.user)

    return render(request, "core/bookings.html", {"bookings": bookings})
