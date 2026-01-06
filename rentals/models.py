from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta

# Custom User
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Property
class Property(models.Model):
    landlord = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'landlord'})
    title = models.CharField(max_length=255)
    rooms = models.PositiveIntegerField()
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    photos = models.ImageField(upload_to='property_photos/')
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('available', 'Available'),
        ('taken', 'Taken')
    ), default='pending')

    def __str__(self):
        return f"{self.title} - {self.rooms} rooms"

# Payment with 72-hour unlock
class Payment(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'tenant'})
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=(
        ('EcoCash', 'EcoCash'),
        ('InnBucks', 'InnBucks'),
        ('OneMoney', 'OneMoney')
    ))
    proof_image = models.ImageField(upload_to='payment_proofs/')
    approved_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=(
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ), default='pending')

    def save(self, *args, **kwargs):
        if self.approved_at and not self.expires_at:
            self.expires_at = self.approved_at + timedelta(hours=72)
        super().save(*args, **kwargs)

    def is_active(self):
        return self.status == 'approved' and self.expires_at and timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.tenant.username} - {self.property.title} ({self.status})"
