from datetime import datetime
from typing import Dict, List, Tuple

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet

from .models import Doctor, Appointment, Patient, TimeSlot


def get_doctor_from_pk(pk: int) -> Doctor:

    return Doctor.objects.get(user=User.objects.get(pk=pk))


def get_patient_from_pk(pk: int) -> Doctor:

    return Patient.objects.get(user=User.objects.get(pk=pk))


def is_user(user, type: str) -> bool:

    return hasattr(user, type)


def serialize_time_slots(time_slots: QuerySet):

    serialized_time_slots = {
        0: 'NOT SELECTED'
    }
    for time_slot in time_slots:
        serialized_time_slots[time_slot.pk] = str(time_slot)

    return serialized_time_slots


def get_available_time_slots_for_doctor(doctor_id: int, date: str) -> Dict:

    doctor = get_doctor_from_pk(doctor_id)
    date = datetime.strptime(date, '%Y-%m-%d')
    booked_time_slot_ids = Appointment.objects.values_list(
        'time_slot').filter(
            doctor=doctor,
            date=date
        )
    available_time_slots = serialize_time_slots(
        TimeSlot.objects.exclude(pk__in=booked_time_slot_ids))

    return available_time_slots


def get_select_field_choices_from_queryset(queryset: QuerySet,
                                           is_user=False) -> List[Tuple]:

    tuples = [
        (0, 'NOT SELECTED')
    ]
    for object in queryset:
        if is_user:
            tuples.append((object.user.id, object))
        else:
            tuples.append((object.id, object))

    return tuples


def require_field_select(value: str) -> None:

    if int(value) < 0:
        error = ValidationError('Please Select this Field')
        raise error


def get_doctor_patients(doctor) -> QuerySet:

    patient_ids = Appointment.objects.values_list(
        'patient').filter(doctor=doctor).distinct()
    patients = Patient.objects.filter(pk__in=patient_ids)
    return patients
