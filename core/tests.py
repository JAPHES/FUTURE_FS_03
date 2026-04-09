from django.contrib.auth.models import AnonymousUser, User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .models import Booking, Service, StylistProfile
from .views import book_service, home, stylist_list


class CoreViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.customer = User.objects.create_user(
            username="customer", password="testpass123"
        )
        stylist_user = User.objects.create_user(
            username="stylist", password="testpass123"
        )
        self.service = Service.objects.create(
            name="Haircut", description="Simple home haircut", price=1500
        )
        self.stylist = StylistProfile.objects.create(
            user=stylist_user,
            full_name="Jane Doe",
            phone="0700000000",
            location="Nairobi",
            bio="Experienced stylist",
            is_available=True,
        )

    def add_session_and_messages(self, request):
        setattr(request, "session", self.client.session)
        setattr(request, "_messages", FallbackStorage(request))

    def test_home_page_loads(self):
        request = self.factory.get(reverse("home"))
        request.user = AnonymousUser()
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, HttpResponse)

    def test_logged_in_user_can_create_booking(self):
        request = self.factory.post(
            reverse("book_service"),
            {
                "service": self.service.id,
                "stylist": self.stylist.id,
                "date": "2026-05-01",
                "time": "10:30",
                "location": "Westlands, Nairobi",
            },
        )
        request.user = self.customer
        self.add_session_and_messages(request)

        response = book_service(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Booking.objects.count(), 1)

    def test_stylist_search_filters_by_location(self):
        request = self.factory.get(reverse("stylists"), {"location": "Nairobi"})
        request.user = AnonymousUser()
        response = stylist_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")
