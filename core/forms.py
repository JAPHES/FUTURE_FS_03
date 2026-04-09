from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Booking, StylistProfile


class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class StylistProfileForm(forms.ModelForm):
    class Meta:
        model = StylistProfile
        fields = [
            "full_name",
            "phone",
            "location",
            "bio",
            "profile_image",
            "is_available",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["service", "stylist", "date", "time", "location"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "location": forms.TextInput(
                attrs={"placeholder": "Enter your home address"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customers should only be able to choose stylists who are available.
        self.fields["stylist"].queryset = StylistProfile.objects.filter(is_available=True)
