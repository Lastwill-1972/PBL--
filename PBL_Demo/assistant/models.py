from django.db import models
from register.models import User


class ChatMessage(models.Model):
    """对话消息模型"""
    ROLE_CHOICES = [
        ('user', '用户'),
        ('assistant', '助手'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages', verbose_name='用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '对话消息'
        verbose_name_plural = '对话消息'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username} - {self.get_role_display()}: {self.content[:50]}'


class ChatSession(models.Model):
    """对话会话模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions', verbose_name='用户')
    title = models.CharField(max_length=100, verbose_name='会话标题', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '对话会话'
        verbose_name_plural = '对话会话'
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.user.username} 的会话 - {self.title or str(self.created_at)[:16]}'
