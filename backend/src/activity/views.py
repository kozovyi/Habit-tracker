from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from activity.models import Activity
from activity.permissions import IsOwner
from activity.serializers import ActivitySerializer, ActivitySerializerCompact, ActivitySerializerDetail

@extend_schema(tags=["Activity"])
class ActivityViewSet(viewsets.ModelViewSet):
    
    queryset = Activity.objects.all()

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).prefetch_related('logs')

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ActivitySerializerDetail
        if self.action == "create":
             return ActivitySerializerCompact
        return ActivitySerializer
    
    def get_permissions(self):
            if self.action in ["retrieve", "update", "partial_update", "destroy"]:
                return [IsAuthenticated(), IsOwner()]
            return [IsAuthenticated()]

    def perform_create(self, serializer):
         serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
         instance.is_archived=True
         instance.save()

