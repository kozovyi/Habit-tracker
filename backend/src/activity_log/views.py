from datetime import date

from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from activity.permissions import IsOwner
from activity_log.models import ActivityLog
from activity_log.serializers import ActivityLogSerializer, ActivityLogSerializerDetail


@extend_schema(tags=["ActivityLog"])
class ActivityLogViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
         return ActivityLog.objects.filter(user=self.request.user).select_related("activity")

    def get_permissions(self):
            if self.action in ["retrieve", "update", "partial_update", "destroy"]:
                return [IsAuthenticated(), IsOwner()]
            return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return ActivityLogSerializer
        return ActivityLogSerializerDetail
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
