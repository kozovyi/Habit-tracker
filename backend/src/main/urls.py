"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from activity.views import ActivityStatisticsViewSet, ActivityViewSet
from activity_log.views import ActivityLogViewSet

router = routers.DefaultRouter()
router.register("activity", ActivityViewSet, basename="activity")
router.register("activity-log", ActivityLogViewSet, basename="activity-log")
router.register("statistics", ActivityStatisticsViewSet, basename="statistics")

urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    
    # swagger
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    
    # auth / user
    path("api/v1/auth/", include('djoser.urls')),
    path("api/v1/auth/token/", include('djoser.urls.jwt')),
    
    # modules
    path("api/v1/", include(router.urls)),
    
]
