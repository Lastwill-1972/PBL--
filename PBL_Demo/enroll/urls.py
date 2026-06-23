from django.urls import path
from . import views

app_name = 'enroll'

urlpatterns = [
    path('event/<int:event_id>/', views.enroll_event, name='enroll_event'),
    path('my/', views.my_enrollments, name='my_enrollments'),
]