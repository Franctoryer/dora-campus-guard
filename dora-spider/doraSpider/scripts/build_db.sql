-- 帖子表
CREATE TABLE IF NOT EXISTS posts (
    id              BIGINT PRIMARY KEY COMMENT '帖子 ID',
    content         TEXT COMMENT '帖子正文',
    uid             BIGINT NOT NULL COMMENT '发帖者 ID',
    is_anonymous    BOOLEAN DEFAULT FALSE COMMENT '是否匿名',
    is_distinguished BOOLEAN DEFAULT FALSE COMMENT '是否精选',
    picture_urls    TEXT COMMENT '图片 URL（每个用逗号隔开）',
    topic_id        BIGINT COMMENT '话题 ID',
    comment_sum     INT DEFAULT 0 COMMENT '评论数',
    like_sum        INT DEFAULT 0 COMMENT '点赞数',
    hot             INT DEFAULT 0 COMMENT '热度',
    tip_sum         INT DEFAULT 0 COMMENT '举报数',
    forward_sum     INT DEFAULT 0 COMMENT '转发数',
    published_at    DATETIME COMMENT '发布时间',
    is_ever_top     BOOLEAN DEFAULT FALSE COMMENT '是否曾经置顶',
    ever_top_end_time DATETIME COMMENT '曾经置顶的结束时间',
    update_time     DATETIME COMMENT '上次更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='帖子数据表';

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    uid BIGINT PRIMARY KEY COMMENT '用户 ID',
    avatar_url TEXT COMMENT '用户头像 URL',
    gender INT DEFAULT 2 COMMENT '性别',
    level INT COMMENT '等级',
    nickname VARCHAR(100) COMMENT '昵称',
    is_admin BOOLEAN DEFAULT FALSE COMMENT '是否是管理员',
    dora_value DOUBLE DEFAULT 0 COMMENT '哆啦值',
    dora_coin DOUBLE DEFAULT 0 COMMENT '哆啦币',
    likes TEXT COMMENT '被哪些人关注 (JSON or comma-separated string)',
    hide_permission BOOLEAN DEFAULT FALSE COMMENT '是否隐藏主页',
    is_anonymous BOOLEAN DEFAULT FALSE COMMENT '是否匿名',
    created_at DATETIME COMMENT '创建时间',
    updated_at DATETIME COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户数据表';