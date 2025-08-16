from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserReadSerializer, UserWriteSerializer
from .permissions import UserRolePermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserRolePermission]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserReadSerializer
        return UserWriteSerializer
