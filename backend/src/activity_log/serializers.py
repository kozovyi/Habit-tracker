from rest_framework import serializers

from activity.models import Activity
from activity_log.models import ActivityLog


class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ("activity", "created_at", "date", "status", "value", "comment")


class ActivityLogShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ("date", "status", "value", "comment")
