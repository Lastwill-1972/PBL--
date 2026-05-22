from django.db import models
from register.models import User
from events.models import Event


class Comment(models.Model):
    """评论模型"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='活动', related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论者', related_name='comments')
    content = models.TextField(verbose_name='评论内容')
    like_count = models.IntegerField(default=0, verbose_name='点赞数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    
    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']


class CommentLike(models.Model):
    """评论点赞模型"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, verbose_name='评论', related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='点赞者', related_name='comment_likes')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')
    
    def __str__(self):
        return f'{self.user.username} 点赞了 {self.comment.id}'
    
    class Meta:
        verbose_name = '评论点赞'
        verbose_name_plural = '评论点赞'
        unique_together = ('comment', 'user')
