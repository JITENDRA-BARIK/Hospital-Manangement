# Hospital Management System Backend

A Django backend for a hospital management system with REST API endpoints for departments, doctors, patients, appointments, and medical records.

## Features
- Django project setup
- Django REST Framework API
- SQLite database by default
- Modular hospital app

## Quick start
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the server:
   ```bash
   python manage.py runserver
   ```

## API endpoints
- `GET /api/health/`
- `GET /api/departments/`
- `GET /api/doctors/`
- `GET /api/patients/`
- `GET /api/appointments/`
- `GET /api/medical-records/`

## Notes
- Authentication is not wired yet.
- You can extend this project with JWT auth, patient portals, billing, pharmacy, and bed management.
