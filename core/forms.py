from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Booking, Service, StylistProfile


class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Keep the form clean and let validation messages appear only when needed.
        for field_name in ["username", "email", "password1", "password2"]:
            self.fields[field_name].help_text = ""

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with that username already exists.")
        return username


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
        fields = ["service", "stylist", "date", "time", "mobile_number", "location"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "mobile_number": forms.TextInput(
                attrs={"placeholder": "Enter your mobile number"}
            ),
            "location": forms.TextInput(
                attrs={"placeholder": "Enter your home address"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customers should only be able to choose stylists who are available.
        self.fields["stylist"].queryset = StylistProfile.objects.filter(is_available=True)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (
                f"{existing_classes} booking-input".strip()
            )


class AdminServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["name", "description", "price", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class AdminBookingStatusForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["status"]


class AdminStylistUpdateForm(forms.ModelForm):
    class Meta:
        model = StylistProfile
        fields = ["full_name", "phone", "location", "is_available"]
