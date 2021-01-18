from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointmentAPI import views

router = DefaultRouter()
router.register('doctor-view', views.DoctorApiView, basename='doctor-view')
router.register('doctor-view/<int:pk>', views.DoctorApiView)


router1 = DefaultRouter()
router1.register('patient-view', views.PatientApiView, basename='patient-view')
router1.register('patient-view/<int:pk>', views.PatientApiView)


router2 = DefaultRouter()
router2.register('appointment-view', views.AppointmentApiView, basename='appointment-view')
router.register('appointment-view/<int:pk>', views.AppointmentApiView)

urlpatterns = [
    path('doctor/', include(router.urls)),
    #path('doctor/<int:pk1>', include(router.urls), ),
    path('patient/', include(router1.urls)),
    #path('patient/<int:pk2>', include(router1.urls)),
    path('appointment/', include(router2.urls)),
    
]
