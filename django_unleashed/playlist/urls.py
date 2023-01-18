from django.urls import path

from playlist import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name="signup"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('playlist/<int:id>', views.playlist, name="playlist"),
]
