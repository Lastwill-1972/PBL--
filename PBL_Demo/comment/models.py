from django.db import models
from register.models import User
from events.models import Event


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='评论内容')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'comment_comment'
        ordering = ['-created_at']
        verbose_name = '评论'
        verbose_name_plural = '评论'

    def __str__(self):
        return f'{self.user.username} - {self.event.title}'