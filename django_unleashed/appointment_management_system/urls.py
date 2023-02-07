from django.urls import path

from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetDoneView, PasswordResetConfirmView,
    PasswordResetCompleteView
)

from .views import (
    AboutView, RegisterView, PatientDetailView,
    PatientListView, ProfileView, UserTypeView,
    ProfileUpdateView, DoctorListView, AppointmentCreateView,
    AppointmentDetailView, AppointmentDeleteView,
    PatientFeelingView, AppointmentAvailableView,
)

from .forms import LoginForm

urlpatterns = [
     path('',
          LoginView.as_view(
               template_name='appointment_management_system/login.html',
               authentication_form=LoginForm),
          name='management-system-login'),
     path('logout/',
          LogoutView.as_view(
               template_name='appointment_management_system/logout.html'),
          name='management-system-logout'),
     path('accounts/password-reset/',
          PasswordResetView.as_view(
               template_name='appointment_management_system/' +
                             'password_reset.html'),
          name='password-reset'),
     path('accounts/password-reset/done',
          PasswordResetDoneView.as_view(
               template_name='appointment_management_system/' +
                             'password_reset_done.html'),
          name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>',
          PasswordResetConfirmView.as_view(
               template_name='appointment_management_system/' +
                             'password_reset_confirm.html'),
          name='password_reset_confirm'),
     path('accounts/password-reset-complete/',
          PasswordResetCompleteView.as_view(
               template_name='appointment_management_system/' +
                             'password_reset_complete.html'),
          name='password_reset_complete'),
     path('about/',
          AboutView.as_view(),
          name='management-system-about'),
     path('register/',
          RegisterView.as_view(),
          name='management-system-register'),
     path('accounts/profile/',
          ProfileView.as_view(),
          name='management-system-profile'),
     path('accounts/profile/update',
          ProfileUpdateView.as_view(),
          name='management-system-update_profile'),
     path('doctors/',
          DoctorListView.as_view(),
          name='management-system-doctors'),
     path('patients/',
          PatientListView.as_view(),
          name='management-system-patients'),
     path('patients/<int:pk>',
          # path(r'^patients/(?P<pk>\d+)$',
          PatientDetailView.as_view(),
          name='management-system-patient-detail'),
     path('patients/feeling/<int:pk>',
          PatientFeelingView.as_view(),
          name='management-system-patient-feeling'),
     path('appointment/new',
          AppointmentCreateView.as_view(),
          name='management-system-schedule-appointment'),
     path('appointment/available',
          AppointmentAvailableView.as_view(),
          name='management-system-appointment-available'),
     path('appointment/<int:pk>',
          AppointmentDetailView.as_view(),
          name='management-system-appointment-detail'),
     path('appointment/<int:pk>/delete',
          AppointmentDeleteView.as_view(),
          name='management-system-appointment-delete'),
     # path('gaccounts/', include('allauth.urls')),
     path('accounts/type',
          UserTypeView.as_view(),
          name='management-system-account-type')
]
