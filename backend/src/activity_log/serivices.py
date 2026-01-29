from datetime import date

from activity_log.exceprions import InvalidDataProvided



class ActivityLogService:

    @staticmethod
    def validate_date_for_create(activity_date: date) -> None:
        if activity_date > date.today():
            raise InvalidDataProvided()
        
    @staticmethod
    def validate_date_for_update(activity_date: date) -> None:
        if activity_date != date.today():
            raise InvalidDataProvided()