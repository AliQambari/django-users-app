from django.contrib.auth.models import AbstractUser
from django.db import models
from .enums import UserRole

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    version = models.PositiveIntegerField(default=1)  # optimistic concurrency
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Auto-increment version on update
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
