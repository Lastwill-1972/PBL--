from django.db import models
from register.models import User
from events.models import Event


class Favorite(models.Model):
    """收藏模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='用户')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='favorites', verbose_name='活动')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'favorite_favorite'
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = [['user', 'event']]

    def __str__(self):
        return f'{self.user.username} 收藏了 {self.event.title}'