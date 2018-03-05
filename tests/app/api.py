from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from resource_permissions.viewsets import PermissionViewSetMixin
from resource_permissions.decorators import detail_route
from tests.app.models import Office, Issue
from tests.app.permissions import OfficePermissions, IssuePermissions
from tests.app.serializers import OfficeSerializer, IssueSerializer, \
    UserSerializer

class OfficeViewSet(PermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    permission_classes = (OfficePermissions,)


class IssueViewSet(PermissionViewSetMixin, viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (IssuePermissions,)

    @detail_route(methods=['get'])
    def start(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def finish(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def cancel(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)


class UserViewSet(PermissionViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer