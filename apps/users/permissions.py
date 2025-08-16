from rest_framework.permissions import BasePermission, SAFE_METHODS
from apps.users.enums import UserRole

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.ADMIN

class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.STAFF

class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.USER

class UserRolePermission(BasePermission):
    """
    - Admin: full CRUD
    - Staff: view + modify others
    - User: view others only
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role = request.user.role

        if role == UserRole.ADMIN:
            return True  # full access

        if role == UserRole.STAFF:
            if request.method in SAFE_METHODS:
                return True
            return True  # staff can also modify

        if role == UserRole.USER:
            return request.method in SAFE_METHODS  # only view

        return False
