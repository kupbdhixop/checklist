from django.contrib.auth.models import User, Group
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import (
    UserSerializer,
    ChecklistSerializer,
    ChecklistDetailSerializer,
    TaskSerializer,
)
from .models import Checklist, Task
from .permissions import IsOwnerOrShared


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ChecklistViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the list view of checklist
    """
    queryset = Checklist.objects.all().order_by('-created')
    serializer_class = ChecklistSerializer
    permission_classes = (IsOwnerOrShared, IsAuthenticated)

    def list(self, request):
        queryset = Checklist.objects.filter(Q(owner=request.user) | Q(shared=request.user))
        serializer = ChecklistSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Checklist.objects.all()
        cl = get_object_or_404(queryset, pk=pk)
        serializer = ChecklistDetailSerializer(cl, context={'request': request})
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint for the list view of Tasks
    """
    queryset = Task.objects.all().filter(completed=False).order_by('-created')
    serializer_class = TaskSerializer
    permission_classes = (IsOwnerOrShared, IsAuthenticated)
