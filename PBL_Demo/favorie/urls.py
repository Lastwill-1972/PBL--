from django.urls import path
from . import views

app_name = 'favorie'

urlpatterns = [
    path('event/<int:event_id>/', views.favorite_event, name='favorite_event'),
]