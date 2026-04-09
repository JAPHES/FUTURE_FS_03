# SalonConnect

SalonConnect is a beginner-friendly Django salon booking platform for customers and stylists.

## Features

- Customer registration, login, and logout using Django authentication
- Stylist profile registration with availability and location
- Service listings and stylist directory
- Booking form for at-home salon appointments
- Booking list for customers and full booking visibility for admins
- Django admin support for services, stylists, and bookings

## Project Structure

- `salonconnect`: Django project settings and root URLs
- `core`: Main application with models, views, forms, templates, and admin setup

## Run the Project

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install django pillow
```

3. Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create an admin user:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Open `http://127.0.0.1:8000/`

## Admin Tasks

- Add salon services
- Manage stylist profiles
- View and update booking status
- Replace placeholder service images by editing a service in the admin panel
