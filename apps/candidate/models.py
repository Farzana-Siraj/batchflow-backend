from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Candidate(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(unique=True)
    link = models.URLField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    current_status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    # Used for concurrency control (batch locking)
    picked_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        indexes = [
            models.Index(fields=["current_status"]),
            models.Index(fields=["created_at"]),
            # composite index for batch selection - batch selection faster in largedata
            models.Index(fields=["current_status", "picked_at"]),
        ]
