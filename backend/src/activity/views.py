from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from activity.models import Activity
from activity.permissions import IsOwner
from activity.serializers import ActivitySerializer, ActivitySerializerCompact, ActivitySerializerDetail

from activity_log.serivices import ActivityStatisticsService
from activity_log.serializers import ActivityIdStatisticsRequestSerializer, ActivityStatisticsRequestSerializer, ActivityStatisticsResponceSerializer, ActivityStreakResponceSerializer

from utils.serivices import validate_by_serializer


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

@extend_schema(tags=["ActivityStatistics"])
class ActivityStatisticsViewSet(viewsets.GenericViewSet):

    queryset = Activity.objects.all()
    permission_classes = [IsOwner]

    def get_serializer_class(self):
        if self.action == 'streak':
            return ActivityIdStatisticsRequestSerializer
        return ActivityStatisticsRequestSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Activity.objects.none() 
        return super().get_queryset().filter(user=self.request.user)

    def _get_safe_activities_or_403(self, validated_data):
        requested_activities = validated_data.get("activities", [])
        safe_activities = [act for act in requested_activities if act.user == self.request.user]

        if len(safe_activities) != len(requested_activities):
            raise PermissionDenied("You are trying to get statistics on other people's activities.")
            
        return safe_activities

    @extend_schema(
        request=ActivityStatisticsRequestSerializer,
        responses=ActivityStatisticsResponceSerializer,
        summary="Get activity statistics",
        description="Returns activity statistics such as completed days, missed days, completion rate."
    )
    def create(self, request, *args, **kwargs):
        validated_data = validate_by_serializer(self.get_serializer_class(), context={"request": request})
        activities = self._get_safe_activities_or_403(validated_data)
        calculated_statistics = ActivityStatisticsService.calculate_statistics({**validated_data, "activities": activities}) # type: ignore
        statistics = ActivityStatisticsResponceSerializer(calculated_statistics)

        return Response(statistics.data, status=status.HTTP_200_OK)


    @extend_schema(
        request=ActivityIdStatisticsRequestSerializer,
        responses=ActivityStreakResponceSerializer,
        summary="Get activity streak",
        description="Returns activity streak."
    )
    @action(detail=False, methods=["post"], url_path="streak")
    def streak(self, request):
        validated_data = validate_by_serializer(self.get_serializer_class(), context={"request": request})
        activities = self._get_safe_activities_or_403(validated_data)
        calculated_statistics_streak = ActivityStatisticsService.calculate_statistics_streak({**validated_data, "activities": activities})  # type: ignore
        statistics_streak = ActivityStreakResponceSerializer(calculated_statistics_streak, many=True)

        return Response(statistics_streak.data, status=status.HTTP_200_OK)
    