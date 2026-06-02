import pymysql

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'pbl_demo',
    'charset': 'utf8mb4'
}

try:
    # 连接数据库
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    
    # 创建 like_like 表
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS `like_like` (
        `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
        `user_id` BIGINT NOT NULL,
        `like_type` VARCHAR(20) NOT NULL,
        `event_id` BIGINT NULL,
        `comment_id` BIGINT NULL,
        `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (`user_id`) REFERENCES `register_user`(`id`) ON DELETE CASCADE,
        FOREIGN KEY (`event_id`) REFERENCES `events_event`(`id`) ON DELETE CASCADE,
        FOREIGN KEY (`comment_id`) REFERENCES `comment_comment`(`id`) ON DELETE CASCADE,
        UNIQUE KEY `unique_like` (`user_id`, `like_type`, `event_id`, `comment_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    
    cursor.execute(create_table_sql)
    connection.commit()
    print("✅ 表 like_like 创建成功！")
    
except Exception as e:
    print(f"❌ 创建表失败: {e}")
    if connection:
        connection.rollback()
finally:
    if connection:
        connection.close()
        print("数据库连接已关闭")