from rest_framework import serializers
from .models import Doctor, UserProfile, Appointment
from passlib.hash import pbkdf2_sha256
#from datetime import date, datetime
import datetime

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
        '''create a new doctor'''
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
        '''update details of existing doctor'''
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
        '''create a new patient'''
        #password = pbkdf2_sha256.encrypt(validated_data['password'], rounds=12000, salt_size=32)
        p = UserProfile(name = validated_data['name'],
                                    email = validated_data['email'],
                                    
                                    )
        p.set_password(validated_data['password'])
        p.save()
        return p

    def update_p(self, pk, validated_data):
        '''update existing patient details'''
        #doc = Doctor.objects.get(pk=pk)
        p = UserProfile.objects.filter(pk=pk).update(**validated_data)
        return p


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'patient_name','doctor_name', 'speciality', 'date','start_time', 'end_time' )
        read_only_fields = ('speciality',)
       
        

    def create(self, validated_data):
        '''create a new appointment'''
        #password = pbkdf2_sha256.encrypt(validated_data['password'], rounds=12000, salt_size=32)
        u = UserProfile.objects.get(pk = validated_data['patient_name'])
        d = Doctor.objects.get(pk = validated_data['doctor_name'])
        dt = validated_data['date']
        doc_name = validated_data['doctor_name']
        pa_name = validated_data['patient_name']
        st = validated_data['start_time'].split(':')
        et = validated_data['end_time'].split(':')
        print(st, et)
        res1 = self.check_for_doc(doc_name, pa_name)
        res2 = self.check_date(dt)
        res3 = self.time_in_range(datetime.time(int(st[0]), int(st[1]), 00))
        res4 = self.time_in_range(datetime.time(int(et[0]), int(et[1]), 00))
        print(res1, res2, res3, res4)
        if res1:
            return('Appointment already exists please select another doctor')
        else:
            if res2:
                if res3 and res4:
                    a = Appointment(patient_name = u,
                            doctor_name = d,
                            speciality = d.speciality,
                            date = validated_data['date'],
                            start_time = validated_data['start_time'],
                            end_time = validated_data['end_time'],
                            )
                    a.save()
                    return a
                else:
                    return('please choose time between 9 AM - 5 PM')
            else:
                return('select a proper date')
            
       
        
        

    def update_a(self, pk, validated_data):
        #doc = Doctor.objects.get(pk=pk)
        a = Appointment.objects.filter(pk=pk).update(**validated_data)
        return a

    def check_for_doc(self,doc_name, pa_name):
        '''check if the doctor appoint exist already for a paticular patient or not'''
        try:
            if Appointment.objects.filter(patient_name = pa_name, doctor_name = doc_name).exists():
                return True
            else:
                return False
        except Appointment.DoesNotExist:
            return False
        
    def check_date(self, dt): 
        '''to check the appointment date is next day or not'''   
        d = dt.split('-')
        #print(d)
        d2 = datetime.datetime(int(d[0]),int(d[1]),int(d[2])).date()
        d1 = datetime.datetime.now().date()
        #print(d1)
        #print(d2)

        return(d2>d1)   
    
    def time_in_range(self,  x):
        """ Return true if x is in the range [start, end] """
        start = datetime.time(9, 0, 0)
        end = datetime.time(17, 0, 0)
        #t = x.split(':')
        if start <= end:
            return start <= x <= end
        else:
            return start <= x or x <= end