from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from events.models import Event
from comment.models import Comment
from django.db import ProgrammingError

def like_event(request, event_id):
    """点赞活动 - AJAX"""
    if not request.session.get('user_id'):
        return JsonResponse({'success': False, 'message': '请先登录'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '无效请求'}, status=400)
    
    event = get_object_or_404(Event, id=event_id)
    user_id = request.session['user_id']
    liked = True
    
    try:
        from like.models import Like
        # 检查是否已经点赞
        existing_like = Like.objects.filter(
            user_id=user_id,
            like_type='event',
            event=event
        ).first()
        
        if existing_like:
            # 取消点赞
            existing_like.delete()
            event.like_count -= 1
            liked = False
        else:
            # 添加点赞
            Like.objects.create(
                user_id=user_id,
                like_type='event',
                event=event
            )
            event.like_count += 1
    except ProgrammingError:
        # 如果 like_like 表不存在，直接增加点赞数（简单模式）
        event.like_count += 1
    except ImportError:
        # 如果模型导入失败，直接增加点赞数
        event.like_count += 1
    
    event.save()
    
    return JsonResponse({
        'success': True,
        'like_count': event.like_count,
        'liked': liked
    })


def like_comment(request, comment_id):
    """点赞评论 - AJAX"""
    if not request.session.get('user_id'):
        return JsonResponse({'success': False, 'message': '请先登录'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '无效请求'}, status=400)
    
    comment = get_object_or_404(Comment, id=comment_id)
    user_id = request.session['user_id']
    liked = True
    
    try:
        from like.models import Like
        # 检查是否已经点赞
        existing_like = Like.objects.filter(
            user_id=user_id,
            like_type='comment',
            comment=comment
        ).first()
        
        if existing_like:
            # 取消点赞
            existing_like.delete()
            comment.like_count -= 1
            liked = False
        else:
            # 添加点赞
            Like.objects.create(
                user_id=user_id,
                like_type='comment',
                comment=comment
            )
            comment.like_count += 1
    except ProgrammingError:
        # 如果 like_like 表不存在，直接增加点赞数
        comment.like_count += 1
    except ImportError:
        # 如果模型导入失败，直接增加点赞数
        comment.like_count += 1
    
    comment.save()
    
    return JsonResponse({
        'success': True,
        'like_count': comment.like_count,
        'liked': liked
    })