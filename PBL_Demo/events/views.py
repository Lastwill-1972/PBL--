from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from register.models import User
from .models import Event
from comment.models import Comment


def public_event_list(request):
    events = Event.objects.filter(is_public=True, status='published').order_by('-start_time')
    events_with_comments = []
    for event in events:
        comments = event.comments.all()[:5]
        events_with_comments.append({
            'event': event,
            'comments': comments,
            'comment_count': event.comments.count()
        })
    return render(request, 'events/public_event_list.html', {'events_with_comments': events_with_comments})


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


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
        status = request.POST.get('status', 'draft')
        is_public = request.POST.get('is_public') == 'on'

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
        event.status = request.POST.get('status', 'draft')
        new_is_public = request.POST.get('is_public') == 'on'
        event.is_public = new_is_public
        event.save()

        if old_is_public and not new_is_public:
            Comment.objects.filter(event=event).delete()

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
        from django.db import connection, ProgrammingError
        try:
            event.delete()
        except ProgrammingError as e:
            # 如果是因为关联表不存在导致的错误，直接用SQL删除
            if 'Table' in str(e) and 'doesn\'t exist' in str(e):
                with connection.cursor() as cursor:
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