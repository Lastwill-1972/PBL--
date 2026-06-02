from django.db import models
from register.models import User
from events.models import Event
from comment.models import Comment


class Like(models.Model):
    """点赞模型"""
    LIKE_TYPE_CHOICES = [
        ('event', '活动'),
        ('comment', '评论'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='用户')
    like_type = models.CharField(max_length=20, choices=LIKE_TYPE_CHOICES, verbose_name='点赞类型')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='likes', null=True, blank=True, verbose_name='活动')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes', null=True, blank=True, verbose_name='评论')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'like_like'
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        unique_together = [['user', 'like_type', 'event', 'comment']]

    def __str__(self):
        if self.like_type == 'event':
            return f'{self.user.username} 点赞了活动 {self.event.title}'
        else:
            return f'{self.user.username} 点赞了评论'