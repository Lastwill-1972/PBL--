from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from register.models import User
from events.models import Event
from .models import Comment
from django.db import connection, ProgrammingError


def login_required(view_func):
    def wrapped_view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapped_view


@login_required
def add_comment(request, event_id):
    """添加评论 - AJAX"""
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()
        except:
            content = request.POST.get('content', '').strip()
        
        if content:
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            event = get_object_or_404(Event, id=event_id)
            comment = Comment.objects.create(
                user=user,
                event=event,
                content=content
            )
            return JsonResponse({
                'success': True,
                'comment_id': comment.id,
                'user_name': user.username,
                'content': content
            })
    
    return JsonResponse({'success': False, 'message': '评论内容不能为空'})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user_id = request.session.get('user_id')

    if comment.user.id != user_id:
        return HttpResponseForbidden('您没有权限删除此评论')

    event_id = comment.event.id
    
    try:
        comment.delete()
    except ProgrammingError as e:
        # 如果是因为关联表不存在导致的错误，直接用SQL删除
        if 'Table' in str(e) and 'doesn\'t exist' in str(e):
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM comment_comment WHERE id = %s", [comment_id])
    
    return redirect('events:event_detail', event_id=event_id)