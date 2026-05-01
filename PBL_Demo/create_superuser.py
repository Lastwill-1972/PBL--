#!/usr/bin/env python
"""创建Django超级管理员用户的脚本"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PBL_Demo.settings')

import django
django.setup()

from register.models import User

def create_superuser():
    print("=" * 50)
    print("      创建Django超级管理员用户")
    print("=" * 50)
    print()
    
    username = input("请输入超级管理员用户名: ").strip()
    if not username:
        print("错误：用户名不能为空")
        return
    
    if User.objects.filter(username=username).exists():
        print(f"错误：用户名 '{username}' 已存在")
        return
    
    college = input("请输入学院: ").strip()
    if not college:
        print("错误：学院不能为空")
        return
    
    student_id = input("请输入学号: ").strip()
    if not student_id:
        print("错误：学号不能为空")
        return
    
    if User.objects.filter(student_id=student_id).exists():
        print(f"错误：学号 '{student_id}' 已存在")
        return
    
    password = input("请输入密码: ").strip()
    if not password:
        print("错误：密码不能为空")
        return
    
    confirm_password = input("请确认密码: ").strip()
    if password != confirm_password:
        print("错误：两次输入的密码不一致")
        return
    
    try:
        user = User.objects.create_superuser(
            username=username,
            email='',
            password=password,
            college=college,
            student_id=student_id
        )
        print()
        print("=" * 50)
        print(f"  超级管理员 '{username}' 创建成功！")
        print("  存储位置：MySQL数据库 pbl_demo")
        print("  登录地址：http://localhost:8000/admin/")
        print("=" * 50)
    except Exception as e:
        print(f"创建失败: {str(e)}")

if __name__ == '__main__':
    create_superuser()