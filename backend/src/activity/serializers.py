from rest_framework import serializers

from activity.models import Activity
from activity_log.serializers import ActivityLogShortSerializer


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("activity_id", "name", "descriprion", "is_archived", "created_at",)


class ActivitySerializerCompact(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ("pk", "name", "descriprion", "is_archived")


class ActivitySerializerDetail(ActivitySerializer):
    last_records = serializers.SerializerMethodField()

    class Meta(ActivitySerializer.Meta):
        fields = ActivitySerializer.Meta.fields + ("last_records",)

    def get_last_records(self, obj):
        logs = obj.logs.all().order_by('-date')[:5]
        return ActivityLogShortSerializer(logs, many=True).data
