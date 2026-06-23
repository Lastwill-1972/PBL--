"""
DeepSeek API 服务层
"""
import requests
import os
from django.conf import settings
from .models import ChatMessage


class DeepSeekService:
    """DeepSeek AI 对话服务"""
    
    API_URL = "https://api.deepseek.com/chat/completions"
    
    SYSTEM_PROMPT = """你是一个PBL活动管理系统的智能助手，以下是本系统的详细信息：

【系统概述】
本系统是一个基于Django的PBL（项目式学习）活动管理平台，专注于帮助学生和教师管理项目式学习活动。

【核心功能模块】

1. 用户管理（register/login）
- 用户注册：需要用户名、密码、学院、学号
- 用户登录：验证用户名和密码
- 用户信息：包含学院、学号等校园信息

2. 活动管理（events）
- 创建活动：填写标题、内容、地点、开始/结束时间
- 活动状态：草稿（draft）、已发布（published）、已取消（cancelled）
- 活动类型：公开活动（可被所有人浏览）、私有活动（仅组织者可见）
- 活动统计：点赞数、收藏数、报名数

3. 互动功能
- 评论（comment）：用户可以对活动发表评论
- 点赞（like）：用户可以点赞活动和评论
- 收藏（favorite）：用户可以收藏感兴趣的活动
- 报名（enroll）：用户可以报名参加公开活动

【用户常用操作流程】
1. 浏览活动：查看公开活动列表，了解活动详情
2. 创建活动：填写活动信息，保存为草稿或直接发布
3. 报名活动：对感兴趣的公开活动进行报名
4. 收藏活动：收藏活动以便以后查看
5. 评论互动：对活动发表评论和看法

【平台特色】
- 专注于PBL项目式学习场景
- 支持活动的完整生命周期管理
- 提供社交互动功能（点赞、收藏、评论）
- 适合高校或培训机构使用

请用友好、专业的方式回答用户问题。当用户询问平台操作时，请详细说明操作步骤；当用户询问PBL相关知识时，请提供专业的学习指导。"""
    
    def __init__(self):
        self.api_key = os.environ.get('DEEPSEEK_API_KEY', getattr(settings, 'DEEPSEEK_API_KEY', ''))
        self.model = os.environ.get('DEEPSEEK_MODEL', getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat'))
    
    def save_message(self, user, role, content):
        """保存对话消息到数据库"""
        ChatMessage.objects.create(user=user, role=role, content=content)
    
    def get_history(self, user, limit=20):
        """获取用户的对话历史"""
        messages = ChatMessage.objects.filter(user=user).order_by('created_at')[:limit]
        return [{'role': m.role, 'content': m.content, 'id': m.id, 'created_at': m.created_at.strftime('%Y-%m-%d %H:%M:%S')} for m in messages]
    
    def delete_message(self, user, message_id):
        """删除单条消息"""
        try:
            message = ChatMessage.objects.get(id=message_id, user=user)
            message.delete()
            return True
        except ChatMessage.DoesNotExist:
            return False
    
    def delete_all_messages(self, user):
        """删除用户所有对话"""
        ChatMessage.objects.filter(user=user).delete()
    
    def get_recent_events(self):
        """获取最近的公开活动数据"""
        try:
            from events.models import Event
            events = Event.objects.filter(
                is_public=True, 
                status='published'
            ).order_by('-start_time')[:5]
            
            event_list = []
            for event in events:
                event_list.append({
                    'id': event.id,
                    'title': event.title,
                    'location': event.location,
                    'start_time': event.start_time.strftime('%Y-%m-%d %H:%M'),
                    'end_time': event.end_time.strftime('%Y-%m-%d %H:%M'),
                    'like_count': event.like_count,
                    'favorite_count': event.favorite_count,
                    'enroll_count': event.enroll_count,
                    'organizer': event.organizer.username
                })
            return event_list
        except Exception:
            return []
    
    def get_event_by_keyword(self, keyword):
        """根据关键词搜索活动"""
        try:
            from events.models import Event
            events = Event.objects.filter(
                is_public=True, 
                status='published',
                title__icontains=keyword
            ).order_by('-start_time')[:5]
            
            event_list = []
            for event in events:
                event_list.append({
                    'id': event.id,
                    'title': event.title,
                    'location': event.location,
                    'start_time': event.start_time.strftime('%Y-%m-%d %H:%M'),
                    'end_time': event.end_time.strftime('%Y-%m-%d %H:%M'),
                    'like_count': event.like_count,
                    'favorite_count': event.favorite_count,
                    'enroll_count': event.enroll_count,
                    'organizer': event.organizer.username
                })
            return event_list
        except Exception:
            return []
    
    def format_events_message(self, events):
        """格式化活动列表为消息文本"""
        if not events:
            return "当前没有公开活动。"
        
        lines = ["以下是当前的公开活动："]
        for i, event in enumerate(events, 1):
            lines.append(f"{i}. 《{event['title']}》")
            lines.append(f"   📍 地点：{event['location']}")
            lines.append(f"   ⏰ 时间：{event['start_time']} ~ {event['end_time']}")
            lines.append(f"   👤 组织者：{event['organizer']}")
            lines.append(f"   ❤️ {event['like_count']} 👍 | ⭐ {event['favorite_count']} 收藏 | 📝 {event['enroll_count']} 报名")
        
        return "\n".join(lines)
    
    def chat(self, user, message):
        """
        发送消息给 DeepSeek API，自动保存对话
        
        Args:
            user: 当前用户对象
            message: 用户当前消息
        
        Returns:
            AI 的回复文本，失败返回错误信息
        """
        if not self.api_key:
            return "错误：未配置 DeepSeek API Key，请在 settings.py 中设置 DEEPSEEK_API_KEY"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        
        history = self.get_history(user)
        for h in history:
            messages.append({"role": h['role'], "content": h['content']})
        
        enhanced_message = message
        
        event_keywords = ['活动', 'event', 'events', '推荐', '报名', '参加', '浏览', '查看']
        if any(keyword in message for keyword in event_keywords):
            events = self.get_recent_events()
            events_info = self.format_events_message(events)
            enhanced_message = f"{message}\n\n【当前活动数据参考】\n{events_info}"
        
        messages.append({"role": "user", "content": enhanced_message})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            self.save_message(user, 'user', message)
            self.save_message(user, 'assistant', ai_response)
            
            return ai_response
        except requests.exceptions.Timeout:
            return "错误：请求超时，请稍后重试"
        except requests.exceptions.RequestException as e:
            return f"错误：API 请求失败 - {str(e)}"
        except (KeyError, IndexError):
            return "错误：解析响应失败"


deepseek_service = DeepSeekService()
