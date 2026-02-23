from datetime import date

import rest_framework
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema
from yaml import serialize

from activity.permissions import IsOwner
from activity_log.models import ActivityLog
from activity_log.serializers import ActivityIdStatisticsRequestSerializer, ActivityLogSerializer, ActivityLogSerializerDetail, ActivityStatisticsRequestSerializer, ActivityStatisticsResponceSerializer, ActivityStreakResponceSerializer
from activity_log.serivices import ActivityStatisticsService
from utils.serivices import validate_by_serializer

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


@extend_schema(tags=["ActivityStatistics"])
class ActivityStatisticsViewSet(viewsets.ViewSet):
    

    @extend_schema(
        request=ActivityStatisticsRequestSerializer,
        responses=ActivityStatisticsResponceSerializer,
        summary="Get activity statistics",
        description="Returns activity statistics such as completed days, missed days, completion rate."
    )
    def create(self, request, *args, **kwargs):
        input_serializer = ActivityStatisticsRequestSerializer
        output_serializer = ActivityStatisticsResponceSerializer

        validated_data = validate_by_serializer(input_serializer, context={"request": request})
        calculated_statistics = ActivityStatisticsService.calculate_statistics(validated_data)
        statistics = output_serializer(calculated_statistics)

        return Response(statistics.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ActivityIdStatisticsRequestSerializer,
        responses=ActivityStreakResponceSerializer,
        summary="Get activity streak",
        description="Returns activity streak."
    )
    @action(detail=False, methods=["post"], url_path="streak")
    def streak(self, request):
        input_serializer = ActivityIdStatisticsRequestSerializer
        output_serializer = ActivityStreakResponceSerializer

        validated_data = validate_by_serializer(input_serializer, context={"request": request})
        calculated_statistics_streak = ActivityStatisticsService.calculate_statistics_streak(validated_data)
        statistics_streak = output_serializer(calculated_statistics_streak, many=True)

        return Response(statistics_streak.data, status=status.HTTP_200_OK)