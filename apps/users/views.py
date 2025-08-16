from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserReadSerializer, UserWriteSerializer
from .permissions import UserRolePermission
from .services import update_user_with_version
from django.core.exceptions import ValidationError

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserRolePermission]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return UserReadSerializer
        return UserWriteSerializer

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        version = request.data.get("version")
        if not version:
            return Response({"detail": "Version is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_user = update_user_with_version(user_id, version, request.data)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        return Response(UserReadSerializer(updated_user).data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
