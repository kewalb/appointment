from rest_framework import serializers
from .models import Doctor, UserProfile, Appointment
from passlib.hash import pbkdf2_sha256
from datetime import date, datetime

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'name', 'email', 'password', 'speciality')
        extra_kwargs = {
            'password' : { 'write_only' : True ,
            'style' : {'input_type':'password'},
            }
        }
        

    def create(self, validated_data):
        password = pbkdf2_sha256.encrypt(validated_data['password'], rounds=12000, salt_size=32)
        d = Doctor(name = validated_data['name'],
                                    email = validated_data['email'],
                                    speciality = validated_data['speciality'],
                                    password = password
                                    )
        #d.set_password(validated_data['password'])
        d.save()
        return d

    def update_doc(self, pk, validated_data):
        #doc = Doctor.objects.get(pk=pk)
        doc = Doctor.objects.filter(pk=pk).update(**validated_data)
        return doc



class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'email', 'password')
        extra_kwargs = {
            'password' : { 'write_only' : True ,
            'style' : {'input_type':'password'},
            }
        }
        

    def create(self, validated_data):
        #password = pbkdf2_sha256.encrypt(validated_data['password'], rounds=12000, salt_size=32)
        p = UserProfile(name = validated_data['name'],
                                    email = validated_data['email'],
                                    
                                    )
        p.set_password(validated_data['password'])
        p.save()
        return p

    def update_p(self, pk, validated_data):
        #doc = Doctor.objects.get(pk=pk)
        p = UserProfile.objects.filter(pk=pk).update(**validated_data)
        return p


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'patient_name','doctor_name', 'speciality', 'date','start_time', 'end_time' )
        read_only_fields = ('speciality',)
       
        

    def create(self, validated_data):
        #password = pbkdf2_sha256.encrypt(validated_data['password'], rounds=12000, salt_size=32)
        u = UserProfile.objects.get(pk = validated_data['patient_name'])
        d = Doctor.objects.get(pk = validated_data['doctor_name'])
        doc_name = validated_data['doctor_name']
        pa_name = validated_data['patient_name']
        st = validated_data['start_time']
        et = validated_data['end_time']
        res1 = self.check_for_doc(doc_name, pa_name)
        print(res1)
        if res1:
            return('Appointment already exists please select another doctor')
        else:
            a = Appointment(patient_name = u,
                        doctor_name = d,
                        speciality = d.speciality,
                        date = validated_data['date'],
                        start_time = validated_data['start_time'],
                        end_time = validated_data['end_time'],
                        )
            a.save()
            return a
       
        
        

    def update_a(self, pk, validated_data):
        #doc = Doctor.objects.get(pk=pk)
        a = Appointment.objects.filter(pk=pk).update(**validated_data)
        return a

    def check_for_doc(self,doc_name, pa_name):
        try:
            if Appointment.objects.filter(patient_name = pa_name, doctor_name = doc_name).exists():
                return True
            else:
                return False
        except Appointment.DoesNotExist:
            return False
        
        
        