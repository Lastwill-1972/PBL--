from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from events.models import Event
from comment.models import Comment
from django.db import connection


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
        # 使用原始SQL检查表是否存在
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'pbl_demo' AND table_name = 'like_like'
            """)
            table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            # 表存在，使用SQL进行点赞/取消点赞操作
            with connection.cursor() as cursor:
                # 检查是否已经点赞
                cursor.execute("""
                    SELECT id FROM like_like 
                    WHERE user_id = %s AND like_type = 'event' AND event_id = %s
                """, [user_id, event_id])
                existing_like = cursor.fetchone()
                
                if existing_like:
                    # 取消点赞
                    cursor.execute("""
                        DELETE FROM like_like 
                        WHERE user_id = %s AND like_type = 'event' AND event_id = %s
                    """, [user_id, event_id])
                    event.like_count -= 1
                    liked = False
                else:
                    # 添加点赞
                    cursor.execute("""
                        INSERT INTO like_like (user_id, like_type, event_id, created_at) 
                        VALUES (%s, 'event', %s, NOW())
                    """, [user_id, event_id])
                    event.like_count += 1
        else:
            # 表不存在，使用session临时存储点赞状态
            likes = request.session.get('temp_likes', {})
            like_key = f"event_{event_id}"
            
            if like_key in likes and likes[like_key] == user_id:
                # 取消点赞
                del likes[like_key]
                event.like_count -= 1
                liked = False
            else:
                # 添加点赞
                likes[like_key] = user_id
                event.like_count += 1
            
            request.session['temp_likes'] = likes
    
    except Exception as e:
        # 如果发生任何错误，使用session方式
        likes = request.session.get('temp_likes', {})
        like_key = f"event_{event_id}"
        
        if like_key in likes and likes[like_key] == user_id:
            del likes[like_key]
            event.like_count -= 1
            liked = False
        else:
            likes[like_key] = user_id
            event.like_count += 1
        
        request.session['temp_likes'] = likes
    
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
        # 使用原始SQL检查表是否存在
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'pbl_demo' AND table_name = 'like_like'
            """)
            table_exists = cursor.fetchone()[0] > 0
        
        if table_exists:
            # 表存在，使用SQL进行点赞/取消点赞操作
            with connection.cursor() as cursor:
                # 检查是否已经点赞
                cursor.execute("""
                    SELECT id FROM like_like 
                    WHERE user_id = %s AND like_type = 'comment' AND comment_id = %s
                """, [user_id, comment_id])
                existing_like = cursor.fetchone()
                
                if existing_like:
                    # 取消点赞
                    cursor.execute("""
                        DELETE FROM like_like 
                        WHERE user_id = %s AND like_type = 'comment' AND comment_id = %s
                    """, [user_id, comment_id])
                    comment.like_count -= 1
                    liked = False
                else:
                    # 添加点赞
                    cursor.execute("""
                        INSERT INTO like_like (user_id, like_type, comment_id, created_at) 
                        VALUES (%s, 'comment', %s, NOW())
                    """, [user_id, comment_id])
                    comment.like_count += 1
        else:
            # 表不存在，使用session临时存储点赞状态
            likes = request.session.get('temp_comment_likes', {})
            like_key = f"comment_{comment_id}"
            
            if like_key in likes and likes[like_key] == user_id:
                # 取消点赞
                del likes[like_key]
                comment.like_count -= 1
                liked = False
            else:
                # 添加点赞
                likes[like_key] = user_id
                comment.like_count += 1
            
            request.session['temp_comment_likes'] = likes
    
    except Exception as e:
        # 如果发生任何错误，使用session方式
        likes = request.session.get('temp_comment_likes', {})
        like_key = f"comment_{comment_id}"
        
        if like_key in likes and likes[like_key] == user_id:
            del likes[like_key]
            comment.like_count -= 1
            liked = False
        else:
            likes[like_key] = user_id
            comment.like_count += 1
        
        request.session['temp_comment_likes'] = likes
    
    comment.save()
    
    return JsonResponse({
        'success': True,
        'like_count': comment.like_count,
        'liked': liked
    })