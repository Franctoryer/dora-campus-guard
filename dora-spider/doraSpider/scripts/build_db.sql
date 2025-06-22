-- 帖子表
CREATE TABLE posts (
    id BIGINT PRIMARY KEY COMMENT '帖子 ID',
    content TEXT COMMENT '帖子正文',
    uid BIGINT NOT NULL COMMENT '发帖者 ID',
    is_anonymous BOOLEAN DEFAULT FALSE COMMENT '是否匿名',
    is_distinguished BOOLEAN DEFAULT FALSE COMMENT '是否精选',
    picture_urls TEXT  DEFAULT NULL COMMENT '图片 URL（逗号分隔）',
    topic_id BIGINT DEFAULT NULL COMMENT '话题 ID',
    comment_sum INT DEFAULT 0 COMMENT '评论数',
    like_sum INT DEFAULT 0 COMMENT '点赞数',
    hot INT DEFAULT 0 COMMENT '热度',
    tip_sum INT DEFAULT 0 COMMENT '举报数',
    forward_sum INT DEFAULT 0 COMMENT '转发数',
    published_at DATETIME COMMENT '发布时间',
    is_ever_top BOOLEAN DEFAULT FALSE COMMENT '是否曾经置顶',
    ever_top_end_time DATETIME DEFAULT NULL COMMENT '曾经置顶结束时间',
    crawled_at DATETIME COMMENT '抓取时间',
    fingerprint CHAR(64) NOT NULL COMMENT '帖子指纹（SHA-256）',
    item_type VARCHAR(10) DEFAULT 'post' COMMENT 'item 类型（post / user）',
    UNIQUE KEY uk_fingerprint (fingerprint) COMMENT '唯一指纹索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='帖子数据表';


-- 用户表
CREATE TABLE users (
    uid BIGINT PRIMARY KEY COMMENT '用户 ID',
    avatar_url VARCHAR(512) DEFAULT NULL COMMENT '头像 URL',
    gender TINYINT DEFAULT 2 COMMENT '性别（0 女，1 男，2 保密）',
    level INT DEFAULT 0 COMMENT '等级',
    nickname VARCHAR(100) DEFAULT '' COMMENT '昵称',
    is_admin BOOLEAN DEFAULT FALSE COMMENT '是否管理员',
    dora_value FLOAT DEFAULT 0 COMMENT '哆啦值',
    dora_coin FLOAT DEFAULT 0 COMMENT '哆啦币',
    hide_permission BOOLEAN DEFAULT FALSE COMMENT '是否隐藏主页',
    is_anonymous BOOLEAN DEFAULT FALSE COMMENT '是否匿名',
    crawled_at DATETIME COMMENT '抓取时间',
    fingerprint CHAR(64) NOT NULL COMMENT '用户指纹（SHA-256）',
    item_type VARCHAR(10) DEFAULT 'user' COMMENT 'item 类型（post/user）',
    UNIQUE KEY uk_fingerprint (fingerprint) COMMENT '唯一指纹索引'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户数据表';
