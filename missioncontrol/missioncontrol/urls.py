"""missioncontrol URL Configuration"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('sensors.urls')),
    path('admin/', admin.site.urls),
]
