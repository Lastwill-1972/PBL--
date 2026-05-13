// 表单验证函数
function validateForm() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
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
    }
    
    return isValid;
}

// 表单提交处理
document.getElementById('login-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    if (validateForm()) {
        // 构建表单数据
        const formData = new FormData();
        formData.append('username', document.getElementById('username').value);
        formData.append('password', document.getElementById('password').value);
        
        // 发送POST请求
        fetch('/login/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 登录成功，可以跳转到首页或其他页面
                alert('登录成功！');
                // 这里可以添加跳转到其他页面的代码
                // window.location.href = '/';
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
            errorMessage.textContent = '登录失败，请稍后重试';
            document.querySelector('.container').insertBefore(errorMessage, document.querySelector('form'));
        });
    }
});
