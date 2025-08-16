from django.contrib.auth.models import AbstractUser
from django.db import models
from .enums import UserRole
from django.core.exceptions import ValidationError

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER
    )
    version = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        # Ensure role is one of the allowed choices (shell problem)
        if self.role not in UserRole.values:
            raise ValidationError({"role": f"Invalid role '{self.role}'. Must be one of {list(UserRole.values)}."})

    
    def save(self, *args, **kwargs):
        self.full_clean()   #run clean()
        # Auto-increment version on update
        if self.pk:
            self.version += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
