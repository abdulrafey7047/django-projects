from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.views.generic import (
    TemplateView, DetailView, ListView,
    DeleteView, CreateView, UpdateView
)

from .models import Appointment, Doctor, Patient
from .utilities import (
    is_user, get_available_time_slots_for_doctor,
    get_patient_from_pk, get_doctor_patients,
    get_select_field_choices_from_queryset
)
from .forms import (
    UserRegisterForm, UserUpdateForm, DoctorUpdateForm,
    PatientUpdateForm, PatientFeelingForm, AppointmentCreateForm,
    UserTypeForm
)


class AboutView(TemplateView):
    template_name = 'appointment_management_system/about.html'


class RegisterView(CreateView):
    template_name = 'appointment_management_system/user_form.html'
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('management-system-login')


class ProfileView(LoginRequiredMixin, ListView):
    model = Appointment
    context_object_name = 'appointments'
    template_name = 'appointment_management_system/profile.html'
    ordering = 'date'
    paginate_by = 5

    def get_queryset(self):
        if is_user(self.request.user, 'doctor'):
            queryset = Appointment.objects.filter(
                doctor=self.request.user.doctor,
                date__gte=timezone.now()).order_by(self.ordering)
            return queryset
        elif is_user(self.request.user, 'patient'):
            queryset = Appointment.objects.filter(
                patient=self.request.user.patient,
                date__gte=timezone.now()).order_by(self.ordering)
            return queryset

    def dispatch(self, request, *args, **kwargs):
        if not (is_user(self.request.user, 'doctor') or
                is_user(self.request.user, 'patient')):
            return redirect('management-system-account-type')
        else:
            return super(ProfileView, self).dispatch(request, *args, **kwargs)


class UserTypeView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserTypeForm
    template_name = 'appointment_management_system/update_account_type.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(request)
        print('SAVED')
        return redirect('management-system-profile')
        # return super().post(request, *args, **kwargs)


class PatientFeelingView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientFeelingForm
    success_url = reverse_lazy('management-system-profile')

    def form_valid(self, form):
        self.object = form.save(pk=self.object.pk)
        return HttpResponseRedirect(self.get_success_url())


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'appointment_management_system/update_profile.html'

    def get(self, request, *args, **kwargs):
        user_update_form = UserUpdateForm(instance=request.user)
        if is_user(request.user, 'doctor'):
            data_update_form = DoctorUpdateForm(instance=request.user.doctor)
        elif is_user(request.user, 'patient'):
            data_update_form = PatientUpdateForm(instance=request.user.patient)

        context = {
            'user_update_form': user_update_form,
            'data_update_form': data_update_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        if is_user(request.user, 'doctor'):
            data_update_form = DoctorUpdateForm(
                request.POST,
                instance=request.user.doctor)
        elif is_user(request.user, 'patient'):
            data_update_form = DoctorUpdateForm(
                request.POST,
                instance=request.user.patient)

        if user_update_form.is_valid() and data_update_form.is_valid():
            user_update_form.save()
            data_update_form.save()
            messages.success(request,
                             'Your Account Information has been Updated!')
            return redirect('management-system-profile')


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentCreateForm
    success_url = reverse_lazy('management-system-profile')
    template_name = 'appointment_management_system/appointment_form.html'

    def get(self, request):
        form = self.form_class()
        form.fields['doctor_user_id'].widget.choices = \
            get_select_field_choices_from_queryset(
                Doctor.objects.all(), is_user=True)
        if request.GET.get('doctor_user_id'):
            form.fields['doctor_user_id'].initial = request.GET.get(
                'doctor_user_id')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        self.object = form.save(self.request)
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentAvailableView(LoginRequiredMixin, TemplateView):
    template_name = 'appointment_management_system/appointment_available.html'

    def post(self, request):
        doctor_id = request.POST.get('doctor_id')
        date = request.POST.get('date')
        available_time_slots = get_available_time_slots_for_doctor(
            doctor_id, date)
        available_time_slots_json = JsonResponse(available_time_slots)
        print(available_time_slots)
        return available_time_slots_json


class DoctorListView(LoginRequiredMixin, ListView):
    model = Doctor
    context_object_name = 'doctors'
    paginate_by = 2

    def get_context_data(self, **kwargs):

        self.queryset = self.get_queryset()
        _, page_obj, obj_list, _ = self.paginate_queryset(
            self.queryset, self.paginate_by)

        if self.request.GET.get('page'):
            page_num = self.request.GET.get('page')
        else:
            page_num = 1

        for doctor in obj_list:
            setattr(doctor, 'num_patients',
                    get_doctor_patients(doctor).count())

        context = super(DoctorListView, self).get_context_data(**kwargs)
        context['doctors'] = obj_list
        context['page_obj'] = page_obj
        context['page'] = page_num
        return context


class PatientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Patient
    context_object_name = 'patients'
    # queryset = get_doctor_patients(self.request.user.doctor)
    paginate_by = 2

    def test_func(self):
        if is_user(self.request.user, 'doctor'):
            return True
        return False

    def get_queryset(self):
        queryset = get_doctor_patients(self.request.user.doctor)
        return queryset

    def get_context_data(self, **kwargs):
        self.queryset = self.get_queryset()
        _, page_obj, obj_list, _ = self.paginate_queryset(
            self.queryset, self.paginate_by)

        if self.request.GET.get('page'):
            page_num = self.request.GET.get('page')
        else:
            page_num = 1

        context = super(PatientListView, self).get_context_data(**kwargs)
        context['patients'] = obj_list
        context['page_obj'] = page_obj
        context['page'] = page_num
        return context


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        object = get_patient_from_pk(pk)
        return object

    def get_context_data(self, **kwargs):
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        if is_user(self.request.user, 'doctor'):
            context['previous_appointments'] = Appointment.objects.filter(
                doctor=self.request.user.doctor,
                patient=self.object,
                date__lt=timezone.now()).order_by('date')
        return context


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                            DeleteView):
    model = Appointment
    success_url = reverse_lazy('management-system-profile')

    def test_func(self):
        appointment = self.get_object()
        if (is_user(self.request.user, 'doctor') and
                appointment.doctor == self.request.user.doctor):
            return True
        elif (is_user(self.request.user, 'patient') and
                appointment.patient == self.request.user.patient):
            return True
        return False
