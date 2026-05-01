from django.db import models
from django.utils import timezone


class User(models.Model):
    """用户模型"""
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=100, verbose_name='密码')
    college = models.CharField(max_length=100, verbose_name='学院')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
