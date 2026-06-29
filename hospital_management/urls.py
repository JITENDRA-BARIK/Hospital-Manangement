from django.contrib import admin
from django.urls import include, path

from apps.hospital.views import (
    appointment_page,
    dashboard_view,
    department_page,
    doctor_page,
    medical_record_page,
    patient_page,
)

urlpatterns = [
    path("", dashboard_view, name="home"),
    path("departments/", department_page, name="departments-page"),
    path("doctors/", doctor_page, name="doctors-page"),
    path("patients/", patient_page, name="patients-page"),
    path("appointments/", appointment_page, name="appointments-page"),
    path("medical-records/", medical_record_page, name="medical-records-page"),
    path("admin/", admin.site.urls),
    path("api/", include("apps.hospital.urls")),
]
