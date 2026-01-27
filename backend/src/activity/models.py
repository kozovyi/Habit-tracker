import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Activity(models.Model):
    activity_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_activities",
        related_query_name="activities"
    )
    name = models.CharField(max_length=255)
    descriprion = models.TextField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activities"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} ({self.user.email})"
    

