# SalonConnect

SalonConnect is a Django-based salon booking platform focused on at-home beauty services. Customers can browse services, discover available stylists, create bookings, and manage their appointments, while admins can monitor bookings and manage the service catalog from a custom dashboard.

## Current Experience

The project now includes a more polished frontend and admin experience:

- Redesigned homepage with stronger calls to action, trust sections, service discovery, and stylist highlights
- Redesigned `services` page with premium catalog-style service cards
- Redesigned `stylists` page with location-based search and stronger profile presentation
- Redesigned login and registration pages with a consistent visual identity
- Redesigned custom admin dashboard with a sidebar shell, metrics, action shortcuts, and activity tracking

## Core Features

- Customer registration, login, and logout using Django authentication
- Stylist profile registration with image upload, location, phone, bio, and availability
- Service listings with pricing and optional uploaded images
- At-home booking flow with service, stylist, date, time, mobile number, and address
- Booking list for customers and full booking visibility for superusers
- Custom admin management pages for bookings, services, and stylists
- Django admin site available at `/admin/`

## Tech Stack

- Python
- Django 4.2.11
- Pillow 12.1.0
- SQLite for local development
- Bootstrap 5 with custom CSS

## Project Structure

- `salonconnect/`: project settings, root URLs, WSGI, and ASGI
- `core/`: models, forms, views, URLs, migrations, and tests
- `templates/`: shared layout, customer pages, auth pages, and custom admin pages
- `static/`: CSS and static image assets
- `media/`: uploaded service and stylist images

## Main Application Flow

1. A visitor opens the homepage and discovers services and stylists.
2. The user registers or logs in.
3. The user chooses a service and stylist, then submits a booking.
4. The booking appears in the customer booking list.
5. A superuser reviews and updates booking status from the custom admin area.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Open the project in your browser:

```text
http://127.0.0.1:8000/
```

## Custom Admin Pages

The custom admin interface is separate from Django's default admin and includes:

- `admin-dashboard/`: overview dashboard
- `admin-dashboard/bookings/`: booking management
- `admin-dashboard/services/`: service management
- `admin-dashboard/stylists/`: stylist management

## Notes

- Uploaded media is served in development when `DEBUG=True`.
- The local database file is `db.sqlite3`.
- Some generated files such as `__pycache__` should generally not be committed.
