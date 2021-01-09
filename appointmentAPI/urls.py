from django.urls import path, include
from rest_framework.routers import DefaultRouter
from appointmentAPI import views

router = DefaultRouter()
router.register('doctor-view', views.DoctorApiView, basename='doctor-view')

router1 = DefaultRouter()
router1.register('patient-view', views.PatientApiView, basename='patient-view')

router2 = DefaultRouter()
router2.register('appointment-view', views.AppointmentApiView, basename='appointment-view')
#router.register('login', views.UserLoginApiView, basename='login-view')

urlpatterns = [
    path('doctor/', include(router.urls)),
    path('doctor/<int:pk>', include(router.urls)),
    path('patient/', include(router1.urls)),
    path('patient/<int:pk>', include(router1.urls)),
    path('appointment/', include(router2.urls)),
    path('appointment/<int:pk>', include(router2.urls)),
    path('appointment/login/', views.UserLoginApiView.as_view()),
]
