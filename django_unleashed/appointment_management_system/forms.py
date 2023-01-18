import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Appointment, Doctor, Patient, TimeSlot
from .utilities import (
    get_select_field_choices_from_queryset,
    require_field_select,
)


class DateInput(forms.DateInput):
    input_type = 'date'


class UserRegisterForm(UserCreationForm):

    CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ]
    email = forms.EmailField()
    register_as = forms.ChoiceField(label='Register As',
                                    choices=CHOICES,
                                    widget=forms.RadioSelect, required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if isinstance(visible.field, forms.ChoiceField):
                visible.field.widget.attrs['class'] = 'form-check-inline'
            else:
                visible.field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True, *args, **kwargs):
        user = super(UserRegisterForm, self).save(
            commit=False, *args, **kwargs)
        user._register_as = self.cleaned_data["register_as"]
        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'register_as']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'email']


class UserTypeForm(forms.ModelForm):

    CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient')
    ]

    type = forms.ChoiceField(label='Select Account Type',
                             choices=CHOICES,
                             widget=forms.RadioSelect, required=True)

    def save(self, request):
        user = request.user
        type = self.cleaned_data["type"]

        if type == 'doctor':
            Doctor.objects.create(user=user)
        elif type == 'patient':
            Patient.objects.create(user=user)

        return user

    class Meta:
        model = User
        fields = ['type']


class DoctorUpdateForm(forms.ModelForm):

    speciality = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(DoctorUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Doctor
        fields = ['firstname', 'lastname', 'study', 'speciality']


class PatientUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PatientUpdateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Patient
        fields = ['firstname', 'lastname']


class PatientFeelingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PatientFeelingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs):

        feeling = self.cleaned_data.get('feeling')
        pk = kwargs.get('pk')
        Patient.objects.filter(pk=pk).update(
            feeling=feeling,
            feeling_updated_datetime=datetime.datetime.today())
        patient = Patient.objects.get(pk=pk)

        return patient

    class Meta:
        model = Patient
        fields = ['feeling']


class AppointmentCreateForm(forms.ModelForm):

    doctor_user_id = forms.CharField(
        label='Select Doctor',
        widget=forms.Select(),
        validators=[require_field_select],)
    patient = forms.HiddenInput()
    date = forms.DateField(required=True, widget=DateInput)
    time_slot_id = forms.CharField(
        label='Select Time Slot',
        widget=forms.Select(
            choices=get_select_field_choices_from_queryset(
                TimeSlot.objects.all())),
        validators=[require_field_select],)

    def __init__(self, *args, **kwargs):
        super(AppointmentCreateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            error = forms.ValidationError('The Date is not Valid')
            raise error
        return date

    def save(self, request):
        doctor = User.objects.get(id=request.POST['doctor_user_id']).doctor
        patient = request.user.patient
        date = self.cleaned_data['date']
        time_slot = TimeSlot.objects.get(pk=int(request.POST['time_slot_id']))

        appointment = Appointment.objects.create(
            doctor=doctor,
            patient=patient,
            date=date,
            time_slot=time_slot
        )
        return appointment

    class Meta:
        model = Appointment
        fields = ['doctor_user_id', 'time_slot_id']
