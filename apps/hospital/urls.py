from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    DepartmentViewSet,
    DoctorViewSet,
    MedicalRecordViewSet,
    PatientViewSet,
    health_check,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"doctors", DoctorViewSet)
router.register(r"patients", PatientViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"medical-records", MedicalRecordViewSet)

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("", include(router.urls)),
]
