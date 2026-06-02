import os
import sys
import django

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PBL_Demo.settings')
sys.path.insert(0, 'd:/PBL/demo/PBL_Demo')
django.setup()

from django.db import connection

# 创建 like_like 表
with connection.cursor() as cursor:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `like_like` (
            `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
            `user_id` BIGINT NOT NULL,
            `like_type` VARCHAR(20) NOT NULL,
            `event_id` BIGINT NULL,
            `comment_id` BIGINT NULL,
            `created_at` DATETIME NOT NULL,
            FOREIGN KEY (`user_id`) REFERENCES `register_user`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`event_id`) REFERENCES `events_event`(`id`) ON DELETE CASCADE,
            FOREIGN KEY (`comment_id`) REFERENCES `comment_comment`(`id`) ON DELETE CASCADE,
            UNIQUE KEY `unique_like` (`user_id`, `like_type`, `event_id`, `comment_id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    print("表 like_like 创建成功！")