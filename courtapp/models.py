from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    ROLE_CHOICES = (
        ('LAWYER', 'Lawyer'),
        ('CLIENT', 'Client'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # ===== COMMON FIELDS =====
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    address = models.TextField()

    # ⚠️ ImageField optional (Pillow install cheyyali)
    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    # ===== LAWYER SPECIFIC =====
    state_bar_council = models.CharField(max_length=100, blank=True, null=True)
    enrollment_number = models.CharField(max_length=50, blank=True, null=True)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    specialization = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)

    # ===== CLIENT SPECIFIC =====
    aadhaar = models.CharField(max_length=12, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class CaseRequest(models.Model):
    client = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='client_cases',
        limit_choices_to={'role': 'CLIENT'}
    )

    lawyer = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='lawyer_cases',
        limit_choices_to={'role': 'LAWYER'}
    )

    case_title = models.CharField(max_length=200)
    description = models.TextField()

    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_title} - {self.status}"

class Hearing(models.Model):
    case = models.ForeignKey(
        CaseRequest,
        on_delete=models.CASCADE,
        related_name='hearings'
    )

    hearing_date = models.DateField()
    hearing_time = models.TimeField()

    note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case.case_title} - {self.hearing_date}"
