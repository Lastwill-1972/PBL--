// 表单验证函数
function validateForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;
    const college = document.getElementById('college').value;
    const studentId = document.getElementById('student-id').value;
    
    // 清除之前的错误信息
    document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
    
    let isValid = true;
    
    // 验证用户名
    if (username.trim() === '') {
        document.getElementById('username-error').textContent = '请输入用户名';
        isValid = false;
    }
    
    // 验证密码
    if (password.trim() === '') {
        document.getElementById('password-error').textContent = '请输入密码';
        isValid = false;
    } else if (password.length < 6) {
        document.getElementById('password-error').textContent = '密码长度至少6位';
        isValid = false;
    }
    
    // 验证确认密码
    if (confirmPassword.trim() === '') {
        document.getElementById('confirm-password-error').textContent = '请确认密码';
        isValid = false;
    } else if (password !== confirmPassword) {
        document.getElementById('confirm-password-error').textContent = '两次输入的密码不一致';
        isValid = false;
    }
    
    // 验证学院
    if (college.trim() === '') {
        document.getElementById('college-error').textContent = '请输入学院';
        isValid = false;
    }
    
    // 验证学号
    if (studentId.trim() === '') {
        document.getElementById('student-id-error').textContent = '请输入学号';
        isValid = false;
    }
    
    return isValid;
}

// 表单提交处理
document.getElementById('register-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (validateForm()) {
        // 构建表单数据
        const formData = new FormData();
        formData.append('username', document.getElementById('username').value);
        formData.append('password', document.getElementById('password').value);
        formData.append('college', document.getElementById('college').value);
        formData.append('student_id', document.getElementById('student-id').value);
        
        // 发送POST请求
        fetch('/register/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 显示成功消息
                const successMessage = document.createElement('div');
                successMessage.className = 'success-message';
                successMessage.textContent = data.message;
                document.querySelector('.container').insertBefore(successMessage, document.querySelector('form'));
                
                // 清空表单
                document.getElementById('register-form').reset();
                
                // 3秒后跳转到登录页面
                setTimeout(() => {
                    window.location.href = '/login/';
                }, 3000);
            } else {
                // 显示错误消息
                if (data.errors) {
                    Object.keys(data.errors).forEach(key => {
                        const errorElement = document.getElementById(`${key}-error`);
                        if (errorElement) {
                            errorElement.textContent = data.errors[key];
                        }
                    });
                } else if (data.message) {
                    const errorMessage = document.createElement('div');
                    errorMessage.className = 'error-message';
                    errorMessage.textContent = data.message;
                    document.querySelector('.container').insertBefore(errorMessage, document.querySelector('form'));
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const errorMessage = document.createElement('div');
            errorMessage.className = 'error-message';
            errorMessage.textContent = '注册失败，请稍后重试';
            document.querySelector('.container').insertBefore(errorMessage, document.querySelector('form'));
        });
    }
});
