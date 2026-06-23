from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from events.models import Event
from enroll.models import Enroll
from register.models import User


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def enroll_event(request, event_id):
    """报名/取消报名活动 - AJAX"""
    if not request.session.get('user_id'):
        return JsonResponse({'success': False, 'message': '请先登录'}, status=401)
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '无效请求'}, status=400)
    
    event = get_object_or_404(Event, id=event_id)
    user_id = request.session['user_id']
    
    if not event.is_public or event.status != 'published':
        return JsonResponse({'success': False, 'message': '只能报名公开活动'}, status=400)
    
    existing_enroll = Enroll.objects.filter(user_id=user_id, event=event).first()
    
    if existing_enroll:
        existing_enroll.delete()
        event.enroll_count -= 1
        enrolled = False
    else:
        Enroll.objects.create(user_id=user_id, event=event)
        event.enroll_count += 1
        enrolled = True
    
    event.save()
    
    return JsonResponse({
        'success': True,
        'enroll_count': event.enroll_count,
        'enrolled': enrolled
    })


@login_required
def my_enrollments(request):
    """查看用户报名的活动列表"""
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    
    enrollments = Enroll.objects.filter(user_id=user_id).order_by('-enrolled_at')
    events = []
    
    for enrollment in enrollments:
        events.append({
            'event': enrollment.event,
            'enrolled_at': enrollment.enrolled_at
        })
    
    return render(request, 'enroll/my_enrollments.html', {'events': events, 'user': user})