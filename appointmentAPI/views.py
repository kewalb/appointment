from django.shortcuts import render

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

    def list(self, request):
        '''return list of all doctors available'''
        d = Doctor.objects.all()
        serializer = self.serializer_class(d, many=True)
        return Response(serializer.data)

    def retrive(self,request, pk=None):
        '''retrive a particular doctor based on id'''
        doc = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(doc, many=True)
        return Response(serializer.data)
        

    def create(self, request):
        '''create a new registration for new Doctor'''
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.create(validated_data = request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        '''update a complete record of doctor or to create a new one from existing'''
        doc = Doctor.objects.get(pk = pk)
        serializer = self.serializer_class(doc, data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data = request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def partial_update(self, request, pk=None):
        '''to make changes to an existing record'''
        doc = Doctor.objects.get(pk = pk)
        serializer = self.serializer_class(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update_doc(validated_data = request.data, pk = pk)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        '''to remove a particular record of doctor based on id'''
        try:
            doc = get_object_or_404(self.queryset, pk = pk)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            op = doc.delete()
            if op:
                return Response('Deleted successfully')
            else:
                return Response('Delete failed')    

            self.delete(doc)
        return Response(status=status.HTTP_204_NO_CONTENT)



class PatientApiView(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = UserProfile.objects.exclude(is_superuser=True)
    #authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    #permission_classes = [IsAuthenticated]

    def create(self, request):
        '''create a new registration for new Doctor'''
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.create(validated_data = request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        '''update a complete record of doctor or to create a new one from existing'''
        doc = UserProfile.objects.get(pk = pk)
        serializer = self.serializer_class(doc, data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data = request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    def partial_update(self, request, pk=None):
        '''to make changes to an existing record'''
        doc = UserProfile.objects.get(pk = pk)
        serializer = self.serializer_class(doc, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.update_p(validated_data = request.data, pk = pk)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        '''to remove a particular record of doctor based on id'''
        try:
            p = get_object_or_404(self.queryset, pk = pk)
        except Doctor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            op = p.delete()
            if op:
                return Response('Deleted successfully')
            else:
                return Response('Delete failed')    

            self.delete(p)
        return Response(status=status.HTTP_204_NO_CONTENT)



class AppointmentApiView(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    
    def list(self, request):
        '''return list of all doctors available'''
        a = Appointment.objects.all()
        serializer = self.serializer_class(a, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def create(self, request):
        '''create a new registration for new Doctor'''
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.create(validated_data = request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrive(self, request, pk=None):
        '''retrive a particular doctor based on id'''
        app = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(app, many=True)
        return Response(serializer.data)
    

class UserLoginApiView(ObtainAuthToken):
    '''Handle user authentication Tokens'''
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
