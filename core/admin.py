from django.contrib import admin

from .models import Booking, Service, StylistProfile


@admin.register(StylistProfile)
class StylistProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "location", "is_available")
    list_filter = ("is_available", "location")
    search_fields = ("full_name", "phone", "location")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer", "stylist", "service", "date", "time", "status")
    list_filter = ("status", "date")
    search_fields = (
        "customer__username",
        "stylist__full_name",
        "service__name",
        "location",
    )
