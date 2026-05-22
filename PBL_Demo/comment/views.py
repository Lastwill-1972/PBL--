from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from register.models import User
from events.models import Event
from .models import Comment, CommentLike


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def add_comment(request, event_id):
    """添加评论"""
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Comment.objects.create(
                event=event,
                user=user,
                content=content
            )
    
    return redirect('events:event_detail', event_id=event_id)


@login_required
def toggle_like(request, comment_id):
    """点赞/取消点赞"""
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    comment = get_object_or_404(Comment, id=comment_id)
    
    like = CommentLike.objects.filter(comment=comment, user=user).first()
    
    if like:
        like.delete()
    else:
        CommentLike.objects.create(comment=comment, user=user)
    
    return redirect('events:event_detail', event_id=comment.event.id)
