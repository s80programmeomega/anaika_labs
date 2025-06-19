from django.http import HttpRequest
from rest_framework import viewsets
from rest_framework import permissions
from .models import CustomUser as User
from .serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = [
        "get",
        "post",
    ]

    def get_permissions(self):
        if self.request.user.is_superuser:
            self.http_method_names = list(
                set(self.http_method_names + ["put", "delete"])
            )
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        request: HttpRequest = self.request
        if request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(id=request.user.id) # type: ignore
