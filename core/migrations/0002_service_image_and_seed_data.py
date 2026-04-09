from django.db import migrations, models


def seed_services(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    sample_services = [
        {
            "name": "Haircut",
            "description": "Classic trims, fades, and home haircut sessions for adults and children.",
            "price": 1200.00,
        },
        {
            "name": "Braiding",
            "description": "Protective braids and neat styling for everyday wear or special occasions.",
            "price": 3500.00,
        },
        {
            "name": "Makeup",
            "description": "Soft glam, bridal, and event makeup done from the comfort of your home.",
            "price": 3000.00,
        },
        {
            "name": "Nails",
            "description": "Manicure, polish application, and nail care for clean and stylish hands.",
            "price": 1800.00,
        },
        {
            "name": "Pedicure",
            "description": "Relaxing foot care, exfoliation, and polish for a fresh pedicure session.",
            "price": 2200.00,
        },
        {
            "name": "Facial",
            "description": "Simple skincare treatments that cleanse, refresh, and brighten the skin.",
            "price": 2500.00,
        },
    ]

    for service_data in sample_services:
        Service.objects.get_or_create(
            name=service_data["name"],
            defaults={
                "description": service_data["description"],
                "price": service_data["price"],
            },
        )


def remove_seeded_services(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Service.objects.filter(
        name__in=["Haircut", "Braiding", "Makeup", "Nails", "Pedicure", "Facial"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="services/"),
        ),
        migrations.RunPython(seed_services, remove_seeded_services),
    ]
