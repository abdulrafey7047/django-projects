from datetime import date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    speciality = models.CharField(max_length=100, null=True, blank=True)
    study = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        if self.firstname:
            return '{} {}'.format(self.firstname, self.lastname)
        return self.user.username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    feeling = models.CharField(max_length=100, null=True, blank=True)
    feeling_updated_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.firstname:
            return '{} {}'.format(self.firstname, self.lastname)
        return self.user.username


class TimeSlot(models.Model):

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self) -> str:
        return f'{self.start_time} - {self.end_time}'


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now,
                            validators=[MinValueValidator(date.today)])
    time_slot = models.ForeignKey(TimeSlot,
                                  on_delete=models.CASCADE, null=True)
