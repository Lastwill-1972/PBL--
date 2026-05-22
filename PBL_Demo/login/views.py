from django.shortcuts import render, redirect
import hashlib
from register.models import User


def login(request):
    """用户登录视图"""
    errors = {}
    error_message = ''
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username:
            errors['username'] = '请输入用户名'
        
        if not password:
            errors['password'] = '请输入密码'
        
        if not errors:
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                try:
                    user = User.objects.get(username=username, password=hashed_password)
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('/events/public/')
                except User.DoesNotExist:
                    error_message = '用户名或密码错误'
    
    return render(request, 'login.html', {'errors': errors, 'error_message': error_message})


def dashboard(request):
    """用户个人中心视图"""
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('/login/')
    
    try:
        user = User.objects.get(id=user_id)
        return render(request, 'dashboard.html', {'user': user})
    except User.DoesNotExist:
        return redirect('/login/')


def logout(request):
    """用户退出登录视图"""
    request.session.flush()
    return redirect('/login/')
