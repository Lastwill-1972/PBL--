from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json
from .services import deepseek_service
from register.models import User


def login_required(view_func):
    """登录验证装饰器"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return JsonResponse({'error': '请先登录'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


def chat_view(request):
    """AI 聊天主页面"""
    if not request.session.get('user_id'):
        return render(request, 'assistant/chat.html', {'error': '请先登录'})
    return render(request, 'assistant/chat.html')


@csrf_exempt
@login_required
def send_message(request):
    """处理发送的消息"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            
            if not message:
                return JsonResponse({'error': '消息不能为空'}, status=400)
            
            user = User.objects.get(id=request.session['user_id'])
            reply = deepseek_service.chat(user, message)
            
            return JsonResponse({'reply': reply})
        except json.JSONDecodeError:
            return JsonResponse({'error': '无效的请求数据'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
    
    return JsonResponse({'error': '仅支持 POST 请求'}, status=405)


@csrf_exempt
@login_required
def get_history(request):
    """获取对话历史"""
    if request.method == 'GET':
        try:
            user = User.objects.get(id=request.session['user_id'])
            history = deepseek_service.get_history(user)
            return JsonResponse({'history': history})
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
    
    return JsonResponse({'error': '仅支持 GET 请求'}, status=405)


@csrf_exempt
@login_required
def delete_message(request, message_id):
    """删除单条消息"""
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=request.session['user_id'])
            success = deepseek_service.delete_message(user, message_id)
            if success:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': '消息不存在'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
    
    return JsonResponse({'error': '仅支持 DELETE 请求'}, status=405)


@csrf_exempt
@login_required
def clear_history(request):
    """清空所有对话"""
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=request.session['user_id'])
            deepseek_service.delete_all_messages(user)
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
    
    return JsonResponse({'error': '仅支持 DELETE 请求'}, status=405)