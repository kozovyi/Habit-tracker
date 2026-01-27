
import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from activity.models import Activity


User = get_user_model()

class ActivityLog(models.Model):
    class ActivityLogStatus(models.TextChoices):
        COMPLETED = 'Виконано'
        PARTIAL = 'Частково'
        SKIPPED = 'Пропущено'

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_avtivities_logs",
    )
    activity = models.ForeignKey(
        to=Activity, 
        on_delete=models.CASCADE, 
        related_name="logs"
    )

    date = models.DateField()
    status = models.CharField(max_length=15, choices=ActivityLogStatus.choices, default=ActivityLogStatus.COMPLETED)

    value = models.PositiveIntegerField(default=0, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('activity', 'date')
        ordering = ["-date"]

    def __str__(self):
        return f"{self.activity.name} log for {self.date}"