from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse
from register.models import User
from .models import Event
from comment.models import Comment


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def public_event_list(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    events = Event.objects.filter(is_public=True, status='published').order_by('-start_time')
    events_with_comments = []
    for event in events:
        comments = event.comments.all()[:5]
        events_with_comments.append({
            'event': event,
            'comments': comments,
            'comment_count': event.comments.count()
        })
    return render(request, 'events/public_event_list.html', {'events_with_comments': events_with_comments, 'user': user})


@login_required
def favorite_events(request):
    """用户收藏的活动列表 - 作为主页"""
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    # 获取用户收藏的活动
    from favorite.models import Favorite
    favorite_event_ids = Favorite.objects.filter(user_id=user_id).values('event_id')
    favorite_events = Event.objects.filter(
        id__in=favorite_event_ids,
        is_public=True,
        status='published'
    ).order_by('-start_time')
    
    return render(request, 'events/favorite_events.html', {'favorite_events': favorite_events, 'user': user})


@login_required
def event_list(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    events = Event.objects.filter(organizer=user)
    return render(request, 'events/event_list.html', {'events': events, 'user': user})


@login_required
def event_create(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        location = request.POST.get('location')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_public = request.POST.get('is_public') == 'on'
        status = request.POST.get('status', 'draft')
        if is_public and status == 'draft':
            status = 'published'

        errors = {}
        if not title:
            errors['title'] = '请输入活动标题'
        if not content:
            errors['content'] = '请输入活动内容'
        if not location:
            errors['location'] = '请输入活动地点'
        if not start_time:
            errors['start_time'] = '请输入开始时间'
        if not end_time:
            errors['end_time'] = '请输入结束时间'

        if errors:
            return render(request, 'events/event_form.html', {
                'errors': errors,
                'event': {
                    'title': title,
                    'content': content,
                    'location': location,
                    'start_time': start_time,
                    'end_time': end_time,
                    'status': status,
                    'is_public': is_public
                },
                'user': user
            })

        Event.objects.create(
            title=title,
            content=content,
            location=location,
            start_time=start_time,
            end_time=end_time,
            organizer=user,
            status=status,
            is_public=is_public
        )
        return redirect('events:event_list')

    return render(request, 'events/event_form.html', {'user': user})


@login_required
def event_edit(request, event_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    event = get_object_or_404(Event, id=event_id)

    if event.organizer.id != user.id:
        return HttpResponseForbidden('您没有权限编辑此活动')

    if request.method == 'POST':
        old_is_public = event.is_public
        event.title = request.POST.get('title')
        event.content = request.POST.get('content')
        event.location = request.POST.get('location')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        new_is_public = request.POST.get('is_public') == 'on'
        event.is_public = new_is_public
        event.status = request.POST.get('status', 'draft')
        if new_is_public and event.status == 'draft':
            event.status = 'published'
        event.save()

        if old_is_public and not new_is_public:
            Comment.objects.filter(event=event).delete()
            from favorite.models import Favorite
            Favorite.objects.filter(event=event).delete()
            from enroll.models import Enroll
            Enroll.objects.filter(event=event).delete()

        return redirect('events:event_list')

    return render(request, 'events/event_form.html', {'event': event, 'user': user})


@login_required
def event_delete(request, event_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    event = get_object_or_404(Event, id=event_id)

    if event.organizer.id != user.id:
        return HttpResponseForbidden('您没有权限删除此活动')

    if request.method == 'POST':
        from django.db import connection, ProgrammingError, IntegrityError, ProgrammingError
        
        try:
            # 先删除关联的评论
            Comment.objects.filter(event=event).delete()
            
            # 再删除关联的收藏
            from favorite.models import Favorite
            Favorite.objects.filter(event=event).delete()
            
            # 删除关联的报名
            from enroll.models import Enroll
            Enroll.objects.filter(event=event).delete()
            
            # 最后删除活动
            event.delete()
        except (IntegrityError, ProgrammingError) as e:
            # 如果遇到外键约束错误，使用SQL直接删除
            with connection.cursor() as cursor:
                # 先删除评论
                cursor.execute("DELETE FROM comment_comment WHERE event_id = %s", [event_id])
                # 删除收藏
                cursor.execute("DELETE FROM favorite_favorite WHERE event_id = %s", [event_id])
                # 删除报名
                cursor.execute("DELETE FROM enroll_enroll WHERE event_id = %s", [event_id])
                # 删除活动
                cursor.execute("DELETE FROM events_event WHERE id = %s", [event_id])
        
        return redirect('events:event_list')

    return render(request, 'events/event_confirm_delete.html', {'event': event, 'user': user})


@login_required
def event_detail(request, event_id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    event = get_object_or_404(Event, id=event_id)
    comments = event.comments.all()
    return render(request, 'events/event_detail.html', {'event': event, 'user': user, 'comments': comments})