from django.shortcuts import render
import datetime

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from .models import Doctor, UserProfile, Appointment
from .serializer import DoctorSerializer, PatientSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# Create your views here.
class DoctorApiView(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

  


class PatientApiView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = UserProfile.objects.exclude(is_superuser=True)
    #authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    



class AppointmentApiView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    
    def create(self, request):
        if request.method == 'POST':
            s = self.serializer_class(data=request.data)
            if s.is_valid():
                d_name = request.data['doctor_name']
                p_name = request.data['patient_name']
                d = request.data['date']
                print(s.data)
                print(p_name)
                print(d_name)
                try:
                #if(datetime.datetime(int(d[0]),int(d[1]),int(d[2])).date() == datetime.datetime.now().date()):
                    if Appointment.objects.filter(patient_name = p_name, doctor_name = d_name, date=d).exists():
                        return Response('cannot appoint with same doctor on same day')
                    else:
                        d = Doctor.objects.get(pk = request.data['doctor_name'])
                        p = UserProfile.objects.get(pk = request.data['patient_name'])
                        a = Appointment(patient_name = p,
                            doctor_name = d,
                            speciality = d.speciality,
                            date = request.data['date'],
                            start_time = request.data['start_time'],
                            end_time = request.data['end_time'],
                            )
                        a.save()
                        return Response(s.data, status=status.HTTP_201_CREATED)
                except Appointment.DoesNotExist:
                    return Response('create a new appointment')
            else:
                return Response(s.errors)


    
    
