from django.contrib.auth.models import User
from django.db import models


class StylistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=100)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to="stylists/", blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["full_name"]

    @property
    def placeholder_image(self):
        # Fall back to local artwork when no profile photo has been uploaded.
        placeholder_map = {
            "Jane Doe": "images/stylists/stylist-1.svg",
            "Mary Wambui": "images/stylists/stylist-2.svg",
            "Aisha Njeri": "images/stylists/stylist-3.svg",
        }
        return placeholder_map.get(self.full_name, "images/stylists/default-stylist.svg")

    def __str__(self):
        return self.full_name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="services/", blank=True, null=True)

    class Meta:
        ordering = ["name"]

    @property
    def placeholder_image(self):
        # Match common service names to bundled fallback artwork.
        placeholder_map = {
            "Haircut": "images/services/haircut.svg",
            "Braiding": "images/services/braiding.svg",
            "Makeup": "images/services/makeup.svg",
            "Nails": "images/services/nails.svg",
            "Pedicure": "images/services/pedicure.svg",
            "Facial": "images/services/facial.svg",
        }
        return placeholder_map.get(self.name, "images/services/default-service.svg")

    def __str__(self):
        return f"{self.name} - KES {self.price}"


class Booking(models.Model):
    # These values drive both customer messaging and admin updates.
    STATUS_PENDING = "Pending"
    STATUS_CONFIRMED = "Confirmed"
    STATUS_COMPLETED = "Completed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_COMPLETED, "Completed"),
    ]

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_bookings"
    )
    stylist = models.ForeignKey(
        StylistProfile, on_delete=models.CASCADE, related_name="bookings"
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    mobile_number = models.CharField(max_length=20, default="", blank=True)
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-time"]

    def __str__(self):
        return (
            f"{self.customer.username} booked {self.service.name} with "
            f"{self.stylist.full_name}"
        )
