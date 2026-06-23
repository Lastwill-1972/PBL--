from django.urls import path
from . import views

app_name = 'assistant'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('history/', views.get_history, name='get_history'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('clear/', views.clear_history, name='clear_history'),
]