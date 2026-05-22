from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('event/<int:event_id>/add/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', views.toggle_like, name='toggle_like'),
]
