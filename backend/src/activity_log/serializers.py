from datetime import date

from rest_framework import serializers
from django.core.exceptions import ValidationError

from activity.models import Activity
from activity_log.models import ActivityLog
from activity_log.serivices import ActivityLogService

class ActivityLogShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ("date", "status", "value", "comment")

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ("activity", "date", "status", "value", "comment")

    def validate(self, attrs):
        request = self.context.get("request")
        if not request:
            return attrs
        
        activity_date = attrs.get("date")

        if request.method == "POST":
            ActivityLogService.validate_date_for_create(activity_date)

        elif request.method in {"PUT", "PATCH"}:
            ActivityLogService.validate_date_for_update(activity_date)

        return attrs

    
class ActivityLogSerializerDetail(serializers.ModelSerializer):
    is_editable = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = ("pk","activity", "date", "status", "value", "comment", "is_editable", "created_at", "updated_at")

    def get_is_editable(self, obj):
        return obj.date == date.today()
