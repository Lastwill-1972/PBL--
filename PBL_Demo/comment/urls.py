from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('add/<int:event_id>/', views.add_comment, name='add_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]