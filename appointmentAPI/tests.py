from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
import json
from django.urls import reverse, reverse_lazy

from .serializer import AppointmentSerializer, DoctorSerializer, PatientSerializer
from .models import UserProfile, Doctor, Appointment

class AppointmentTestCase(APITestCase):

    correct = {
        'patient_name' : 5, 
        'doctor_name' : 3, 
        'date' : '2021-01-15',
        'start_time':'10:00:00',
        'end_time':'11:00:00'
        }
   
    
    u = UserProfile.objects.get(pk = 6)
    d = Doctor.objects.get(pk = 3)
    a = Appointment(patient_name = u, doctor_name = d, date = '2021-01-15',start_time = '10:00:00',end_time = '11:00:00')

    def test_appointment(self):
        data = {'patient_name':'6', 'doctor_name':'3', 'date':'2021-01-15', 'start_time':'10:00:00', 'end_time':'11:00:00'}
        response = self.client.post('/api/appointment/appointment-view/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_appointment_list(self):
        response = self.client.get('/api/appointment/appointment-view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_appointment_detail(self):
        a = Appointment.objects.all()
        if a:
            response = self.client.get('/api/appointment/appointment-view/', kwargs={'pk': self.a.pk})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(json.loads(response.content), {
        'patient_name' : '6', 
        'doctor_name' : '3', 
        'date' : '2021-01-15',
        'start_time':'10:00:00',
        'end_time':'11:00:00'
        })
    
    def test_appointment_update(self):
        response = self.client.put(
            '/api/appointment/appointment-view/<int:pk>/', kwargs={'pk': self.a.pk},
            data = self.correct,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def delete_appointment(self):
        response = self.Appointment.delete(
           '/api/appointment/appointment-view/' , kwargs={'pk': self.a.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class UserTestCase(APITestCase):

    def test_user(self):
        data = {'email':'patient456@gmail.com', 'name':'patient456', 'password':'patient000'}
        response = self.client.post('/api/patient/patient-view/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_list(self):
        response = self.client.get('/api/patient/patient-view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_detail(self):
        a = UserProfile.objects.all()
        if a:
            response = self.client.get('/api/appointment/appointment-view/', kwargs={'pk': self.UserProfile.pk})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_patient(self):
        response = self.UserProfile.delete(
           '/api/patient/patientt-view/' , kwargs={'pk': self.patient.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class DoctorTestCase(APITestCase):

    doctor = Doctor.objects.create(name = 'doc4', email='doc4@gmail.com', speciality='xyz', password='doc4567')

    def test_doctor(self):
        data = {'email':'doc456@gmail.com', 'name':'doc456', 'password':'doctor456', 'speciality':'homeopathy'}
        response = self.client.post('/api/doctor/doctor-view/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_doctor_list(self):
        response = self.client.get('/api/doctor/doctor-view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_detail(self):
        d = Doctor.objects.all()
        if d:
            response = self.client.get('/api/appointment/appointment-view/', kwargs={'pk': self.doctor.pk})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def delete_doctor(self):
        response = self.Doctor.delete(
           '/api/doctor/doctor-view/' , kwargs={'pk': self.doctor.pk})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)