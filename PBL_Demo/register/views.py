from django.shortcuts import render, redirect
import hashlib
from .models import User


def register(request):
    """用户注册视图"""
    errors = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        college = request.POST.get('college')
        student_id = request.POST.get('student_id')
        
        if not username:
            errors['username'] = '请输入用户名'
        elif User.objects.filter(username=username).exists():
            errors['username'] = '用户名已存在'
        
        if not password:
            errors['password'] = '请输入密码'
        elif len(password) < 6:
            errors['password'] = '密码长度至少6位'
        
        if not confirm_password:
            errors['confirm_password'] = '请确认密码'
        elif password != confirm_password:
            errors['confirm_password'] = '两次输入的密码不一致'
        
        if not college:
            errors['college'] = '请输入学院'
        
        if not student_id:
            errors['student_id'] = '请输入学号'
        elif User.objects.filter(student_id=student_id).exists():
            errors['student_id'] = '学号已存在'
        
        if not errors:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            try:
                user = User.objects.create(
                    username=username,
                    password=hashed_password,
                    college=college,
                    student_id=student_id
                )
                return redirect('/login/')
            except Exception as e:
                errors['general'] = f'注册失败: {str(e)}'
    
    return render(request, 'register.html', {'errors': errors})
