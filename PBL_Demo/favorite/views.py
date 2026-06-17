from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from events.models import Event
from favorite.models import Favorite


def favorite_event(request, event_id):
    """收藏/取消收藏活动 - AJAX"""
    if not request.session.get('user_id'):
        return JsonResponse({'success': False, 'message': '请先登录'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '无效请求'}, status=400)
    
    event = get_object_or_404(Event, id=event_id)
    user_id = request.session['user_id']
    
    # 检查活动是否公开
    if not event.is_public or event.status != 'published':
        return JsonResponse({'success': False, 'message': '只能收藏公开活动'}, status=400)
    
    # 检查是否已经收藏
    existing_favorite = Favorite.objects.filter(
        user_id=user_id,
        event=event
    ).first()
    
    if existing_favorite:
        # 取消收藏
        existing_favorite.delete()
        event.favorite_count -= 1
        favorited = False
    else:
        # 添加收藏
        Favorite.objects.create(
            user_id=user_id,
            event=event
        )
        event.favorite_count += 1
        favorited = True
    
    event.save()
    
    return JsonResponse({
        'success': True,
        'favorite_count': event.favorite_count,
        'favorited': favorited
    })