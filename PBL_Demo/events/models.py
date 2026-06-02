from django.db import models
from register.models import User


class Event(models.Model):
    """活动模型"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
        ('cancelled', '已取消'),
    ]

    title = models.CharField(max_length=200, verbose_name='活动标题')
    content = models.TextField(verbose_name='活动内容')
    location = models.CharField(max_length=200, verbose_name='活动地点')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='组织者', related_name='organized_events')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='状态')
<<<<<<< HEAD
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
=======
>>>>>>> upstream/main
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '活动'
        verbose_name_plural = '活动'
        ordering = ['-created_at']