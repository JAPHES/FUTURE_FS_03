from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.service_list, name="services"),
    path("stylists/", views.stylist_list, name="stylists"),
    path("book/", views.book_service, name="book_service"),
    path("bookings/", views.booking_list, name="booking_list"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("register/", views.register, name="register"),
    path("register/stylist/", views.stylist_register, name="stylist_register"),
]
