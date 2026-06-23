from django.db import models
from register.models import User
from events.models import Event


class Enroll(models.Model):
    """报名模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolls', verbose_name='用户')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='enrolls', verbose_name='活动')
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name='报名时间')

    class Meta:
        db_table = 'enroll_enroll'
        verbose_name = '报名'
        verbose_name_plural = '报名'
        unique_together = [['user', 'event']]

    def __str__(self):
        return f'{self.user.username} 报名了 {self.event.title}'