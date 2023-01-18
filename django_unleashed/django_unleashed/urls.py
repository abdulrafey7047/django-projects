from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('playlist/', include('playlist.urls')),
    path('ams', include('appointment_management_system.urls'))
]
