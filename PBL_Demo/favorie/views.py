from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from events.models import Event
from django.db import connection


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
    
    favorited = True
    
    try:
        # 使用原始SQL检查表是否存在
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'pbl_demo' AND table_name = 'favorie_favorite'
            """)
            table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            # 表存在，使用SQL进行收藏/取消收藏操作
            with connection.cursor() as cursor:
                # 检查是否已经收藏
                cursor.execute("""
                    SELECT id FROM favorie_favorite 
                    WHERE user_id = %s AND event_id = %s
                """, [user_id, event_id])
                existing_favorite = cursor.fetchone()
                
                if existing_favorite:
                    # 取消收藏
                    cursor.execute("""
                        DELETE FROM favorie_favorite 
                        WHERE user_id = %s AND event_id = %s
                    """, [user_id, event_id])
                    event.favorite_count -= 1
                    favorited = False
                else:
                    # 添加收藏
                    cursor.execute("""
                        INSERT INTO favorie_favorite (user_id, event_id, created_at) 
                        VALUES (%s, %s, NOW())
                    """, [user_id, event_id])
                    event.favorite_count += 1
        else:
            # 表不存在，使用session临时存储收藏状态
            favorites = request.session.get('temp_favorites', {})
            favorite_key = f"event_{event_id}"
            
            if favorite_key in favorites and favorites[favorite_key] == user_id:
                # 取消收藏
                del favorites[favorite_key]
                event.favorite_count -= 1
                favorited = False
            else:
                # 添加收藏
                favorites[favorite_key] = user_id
                event.favorite_count += 1
            
            request.session['temp_favorites'] = favorites
    
    except Exception as e:
        # 如果发生任何错误，使用session方式
        favorites = request.session.get('temp_favorites', {})
        favorite_key = f"event_{event_id}"
        
        if favorite_key in favorites and favorites[favorite_key] == user_id:
            del favorites[favorite_key]
            event.favorite_count -= 1
            favorited = False
        else:
            favorites[favorite_key] = user_id
            event.favorite_count += 1
        
        request.session['temp_favorites'] = favorites
    
    event.save()
    
    return JsonResponse({
        'success': True,
        'favorite_count': event.favorite_count,
        'favorited': favorited
    })