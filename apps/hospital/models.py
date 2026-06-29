from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Department(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Doctor(TimestampedModel):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    specialization = models.CharField(max_length=120)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctors")

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


class Patient(TimestampedModel):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Appointment(TimestampedModel):
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("no_show", "No Show"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    reason = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-appointment_date"]

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date:%Y-%m-%d %H:%M}"


class MedicalRecord(TimestampedModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medical_records")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_records")
    visit_date = models.DateTimeField()
    diagnosis = models.TextField()
    prescription = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-visit_date"]

    def __str__(self):
        return f"Record for {self.patient} on {self.visit_date:%Y-%m-%d}"
