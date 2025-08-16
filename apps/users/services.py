from django.db import transaction
from django.core.exceptions import ValidationError
from .models import User

def update_user_with_version(user_id, version, data):
    """
    Update a user only if version matches.
    Raises ValidationError if versions conflict.
    """
    with transaction.atomic():
        user = User.objects.select_for_update().filter(id=user_id, version=version).first()
        if not user:
            raise ValidationError("Conflict: user was modified by someone else.")

        for attr, value in data.items():
            if attr == "password":
                user.set_password(value)
            else:
                setattr(user, attr, value)

        user.save()
        return user
