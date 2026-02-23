from datetime import date

from rest_framework import serializers
from django.core.exceptions import ValidationError

from drf_spectacular.utils import extend_schema_field

from activity.models import Activity
from activity_log.models import ActivityLog
from activity_log.serivices import ActivityLogService, ActivityStatisticsService


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

    @extend_schema_field(serializers.BooleanField)
    def get_is_editable(self, obj) -> bool:
        return obj.date == date.today()

class ActivityIdStatisticsRequestSerializer(serializers.Serializer):
    activity_id = serializers.PrimaryKeyRelatedField(
        queryset=Activity.objects.all(),
        write_only=True,
        source = "activities",
        many = True,
    )

class ActivityStatisticsRequestSerializer(ActivityIdStatisticsRequestSerializer):
    period_to = serializers.DateField()
    period_from = serializers.DateField()

    def validate(self, data):
        return ActivityStatisticsService.validate_date_range(self, data)

class ActivityStatisticsResponceSerializer(serializers.Serializer):
    completed_days = serializers.IntegerField(min_value=0)
    missed_days = serializers.IntegerField(min_value=0)
    completion_rate = serializers.FloatField(max_value=100, min_value=0)


class ActivityStreakResponceSerializer(serializers.Serializer):
    activity = serializers.PrimaryKeyRelatedField(read_only=True)
    streak = serializers.IntegerField(min_value=0)
