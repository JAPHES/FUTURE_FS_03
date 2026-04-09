from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="services"),
    path("stylists/", views.stylist_list, name="stylists"),
    path("book/", views.book_service, name="book_service"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-dashboard/bookings/", views.admin_bookings, name="admin_bookings"),
    path("admin-dashboard/services/", views.admin_services, name="admin_services"),
    path("admin-dashboard/stylists/", views.admin_stylists, name="admin_stylists"),
    path("register/", views.register, name="register"),
    path("register/stylist/", views.stylist_register, name="stylist_register"),
]
