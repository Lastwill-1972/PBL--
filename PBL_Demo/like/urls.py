from django.urls import path
from . import views

app_name = 'like'

urlpatterns = [
    path('event/<int:event_id>/', views.like_event, name='like_event'),
    path('comment/<int:comment_id>/', views.like_comment, name='like_comment'),
]