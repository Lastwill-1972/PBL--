from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
<<<<<<< HEAD
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
=======
    # 公开活动列表（优先于动态路由）
    path('public/', views.public_events, name='public_events'),
    # 创建活动
    path('create/', views.event_create, name='event_create'),
    # 我的活动列表
    path('', views.event_list, name='event_list'),
    # 动态路由放在最后
>>>>>>> 7c97f9c (feat:评论功能)
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('<int:event_id>/delete/', views.event_delete, name='event_delete'),
]