from asyncio import streams
from collections import defaultdict
from datetime import date, timedelta
from datetime import datetime
from unittest import result

from django.db.models import Avg, Sum, Count, When, Q

from activity.models import Activity
from activity_log.exceprions import InvalidDataProvided, InvalidDateRange, InvalidPeriodToDate
from activity_log.models import ActivityLog



class ActivityLogService:

    @staticmethod
    def validate_date_for_create(activity_date: date) -> None:
        if activity_date > date.today():
            raise InvalidDataProvided()
        
    @staticmethod
    def validate_date_for_update(activity_date: date) -> None:
        if activity_date != date.today():
            raise InvalidDataProvided()
        
    

class ActivityStatisticsService:

    @staticmethod
    def _get_complated_missed_days(period_from, period_to, activities):
        queryset = ActivityLog.objects.filter(
            activity__in=activities,
            date__range=[period_from, period_to]
        ).aggregate(complated = Count('id', filter=Q(status=ActivityLog.ActivityLogStatus.COMPLETED)),
                     missed = Count('id', filter=Q(status=ActivityLog.ActivityLogStatus.SKIPPED)),
                     total_records = Count('id')
        )
        
        end_date_for_missed = min(period_to, date.today() - timedelta(days=1))
        total_days = (end_date_for_missed - period_from).days + 1

        completed_days = queryset['complated']
        missed_days = queryset['missed'] + total_days - queryset['total_records']
        completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0
        return (completed_days,missed_days,completion_rate)



    @staticmethod
    def _get_streak(activities) -> list:
        
        results = []
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        queryset = ActivityLog.objects.filter(
            activity__in = activities,
            status = ActivityLog.ActivityLogStatus.COMPLETED
        ).order_by("activity_id", "-date")

        logs: defaultdict[str, list] = defaultdict(list)
        for log in queryset:
            logs[log.activity_id].append(log.date) #type: ignore


        for activity in activities:
            activity_dates = logs.get(activity.pk, [])
            streak = 0

            if not activity_dates or activity_dates[0] not in [today, yesterday]:
                results.append({"activity": activity, "streak": 0})
                continue
            
            expected_date = activity_dates[0]
            for record in activity_dates:
                    if record == expected_date:
                        streak += 1
                        expected_date -= timedelta(days=1) 
                    elif record < expected_date:
                        break
                
            results.append({"activity": activity, "streak": streak})
        
        return results
    
    @staticmethod
    def validate_date_range(instance, data):
        if data["period_to"] > datetime.now().date():
            raise InvalidPeriodToDate()
        if data["period_from"] >= data["period_to"]:
            raise InvalidDateRange()
        return data
    
    @classmethod
    def calculate_statistics(cls, data):

        period_from = data["period_from"]
        period_to = data["period_to"]
        activities=data["activities"]

        completed_days,missed_days,completion_rate=cls._get_complated_missed_days(period_from, period_to, activities)

        return {
            "completed_days": completed_days,
            "missed_days": missed_days,
            "completion_rate": completion_rate,
        }


    
        
    @classmethod
    def calculate_statistics_streak(cls, data):
        activities=data["activities"]
        streak = cls._get_streak(activities)
       
        return streak
        
