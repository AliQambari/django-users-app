from django.db import models

class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    STAFF = 'STAFF', 'Staff'
    USER = 'USER', 'User'
