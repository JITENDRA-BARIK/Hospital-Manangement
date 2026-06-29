from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Appointment, Department, Doctor, MedicalRecord, Patient
from .serializers import (
    AppointmentSerializer,
    DepartmentSerializer,
    DoctorSerializer,
    MedicalRecordSerializer,
    PatientSerializer,
)


@api_view(["GET"])
def health_check(request):
    return Response({"status": "ok", "message": "Hospital Management API is running"})


def _dt(value):
    return value.strftime("%d %b %Y, %I:%M %p") if value else "—"


def dashboard_view(request):
    departments = Department.objects.count()
    doctors = Doctor.objects.count()
    patients = Patient.objects.count()
    appointments = Appointment.objects.count()
    records = MedicalRecord.objects.count()

    recent_appointments = Appointment.objects.select_related("patient", "doctor").order_by("-appointment_date")[:5]
    recent_patients = Patient.objects.order_by("-created_at")[:5]
    active_departments = Department.objects.annotate(total_doctors=Count("doctors")).order_by("name")[:4]

    return render(
        request,
        "home.html",
        {
            "departments": departments,
            "doctors": doctors,
            "patients": patients,
            "appointments": appointments,
            "records": records,
            "recent_appointments": recent_appointments,
            "recent_patients": recent_patients,
            "active_departments": active_departments,
        },
    )


def department_page(request):
    departments = Department.objects.annotate(total_doctors=Count("doctors")).order_by("name")
    rows = [
        [dept.name, dept.description or "—", str(dept.total_doctors), _dt(dept.created_at)]
        for dept in departments
    ]
    return render(
        request,
        "table_page.html",
        {
            "title": "Departments",
            "subtitle": "Hospital departments and their doctor counts.",
            "headers": ["Name", "Description", "Doctors", "Created"],
            "rows": rows,
        },
    )


def doctor_page(request):
    doctors = Doctor.objects.select_related("department").order_by("first_name", "last_name")
    rows = [
        [
            f"Dr. {doctor.first_name} {doctor.last_name}",
            doctor.specialization,
            doctor.department.name if doctor.department else "—",
            doctor.phone or "—",
            doctor.email or "—",
        ]
        for doctor in doctors
    ]
    return render(
        request,
        "table_page.html",
        {
            "title": "Doctors",
            "subtitle": "Doctor profiles and department assignments.",
            "headers": ["Name", "Specialization", "Department", "Phone", "Email"],
            "rows": rows,
        },
    )


def patient_page(request):
    patients = Patient.objects.order_by("first_name", "last_name")
    rows = [
        [
            f"{patient.first_name} {patient.last_name}",
            patient.gender or "—",
            patient.phone or "—",
            patient.email or "—",
            _dt(patient.created_at),
        ]
        for patient in patients
    ]
    return render(
        request,
        "table_page.html",
        {
            "title": "Patients",
            "subtitle": "Registered patients in the hospital system.",
            "headers": ["Name", "Gender", "Phone", "Email", "Created"],
            "rows": rows,
        },
    )


def appointment_page(request):
    appointments = Appointment.objects.select_related("patient", "doctor").order_by("-appointment_date")
    rows = [
        [
            str(appointment.patient),
            str(appointment.doctor),
            _dt(appointment.appointment_date),
            appointment.status.replace("_", " ").title(),
            appointment.reason,
        ]
        for appointment in appointments
    ]
    return render(
        request,
        "table_page.html",
        {
            "title": "Appointments",
            "subtitle": "Scheduled visits and booking status.",
            "headers": ["Patient", "Doctor", "Date", "Status", "Reason"],
            "rows": rows,
        },
    )


def medical_record_page(request):
    records = MedicalRecord.objects.select_related("patient", "doctor").order_by("-visit_date")
    rows = [
        [
            str(record.patient),
            str(record.doctor) if record.doctor else "—",
            _dt(record.visit_date),
            record.diagnosis,
        ]
        for record in records
    ]
    return render(
        request,
        "table_page.html",
        {
            "title": "Medical Records",
            "subtitle": "Clinical notes and diagnosis history.",
            "headers": ["Patient", "Doctor", "Visit Date", "Diagnosis"],
            "rows": rows,
        },
    )


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related("department").all()
    serializer_class = DoctorSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related("patient", "doctor").all()
    serializer_class = AppointmentSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.select_related("patient", "doctor").all()
    serializer_class = MedicalRecordSerializer
