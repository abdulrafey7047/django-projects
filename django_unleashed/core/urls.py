from django.urls import path

from core import views


urlpatterns = [
    path('', views.home, name="core-home"),
    path('resume/', views.resume, name="core-resume"),
]
