from sqlalchemy import Column, BigInteger, Integer, String, Text, Boolean, DateTime, UniqueConstraint, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

from sqlalchemy import Column, BigInteger, Integer, String, Text, DateTime, Boolean, UniqueConstraint
from datetime import datetime

class Post(Base):
    """
    帖子表 posts
    """
    __tablename__ = "posts"
    __table_args__ = (
        UniqueConstraint("fingerprint", name="uk_fingerprint"),
        {"comment": "帖子数据表"}
    )

    id = Column(BigInteger, primary_key=True, comment="帖子 ID")
    content = Column(Text, comment="帖子正文")
    uid = Column(BigInteger, nullable=False, comment="发帖者 ID")
    is_anonymous = Column(Boolean, default=False, comment="是否匿名")
    is_distinguished = Column(Boolean, default=False, comment="是否精选")
    picture_urls = Column(Text, nullable=True, comment="图片 URL（逗号分隔）")
    risky = Column(Boolean, default=False, comment="是否有风险")
    topic_id = Column(BigInteger, nullable=True, comment="话题 ID")
    comment_sum = Column(Integer, default=0, comment="评论数")
    like_sum = Column(Integer, default=0, comment="点赞数")
    hot = Column(Integer, default=0, comment="热度")
    tip_sum = Column(Integer, default=0, comment="举报数")
    forward_sum = Column(Integer, default=0, comment="转发数")
    dun_num = Column(Integer, default=0, comment="蹲数")
    school_id = Column(BigInteger, nullable=True, comment="学校 ID")
    is_fee = Column(Boolean, default=False, comment="是否收费")
    origin = Column(Integer, default=0, comment="来源")
    ad_level = Column(Integer, default=0, comment="广告等级")
    settled = Column(Boolean, default=False, comment="是否已解决")
    published_at = Column(DateTime, comment="发布时间")
    sentiment_label = Column(Integer, comment="情感类型")
    sentiment_confidence = Column(Float, comment="情感预测置信度")
    abnormal_index = Column(Integer, comment="异常预警指数")
    is_ever_top = Column(Boolean, default=False, comment="是否曾经置顶")
    ever_top_end_time = Column(DateTime, nullable=True, comment="曾经置顶结束时间")
    crawled_at = Column(DateTime, default=datetime.utcnow, comment="抓取时间")
    fingerprint = Column(String(64), nullable=False, comment="帖子指纹（SHA-256）")
    item_type = Column(String(10), default="post", comment="item 类型（post / user）")




class User(Base):
    """
    用户表 users
    """
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("fingerprint", name="uk_fingerprint"),
        {"comment": "用户数据表"}
    )

    uid = Column(BigInteger, primary_key=True, comment="用户 ID")
    avatar_url = Column(String(512), nullable=True, comment="头像 URL")
    gender = Column(Integer, default=2, comment="性别（0 女，1 男，2 保密）")
    level = Column(Integer, default=0, comment="等级")
    nickname = Column(String(100), default="", comment="昵称")
    is_admin = Column(Boolean, default=False, comment="是否管理员")
    school_id = Column(BigInteger, nullable=True, comment="学校 ID")
    dora_coin = Column(Float, default=0.0, comment="哆啦币")
    hide_permission = Column(Boolean, default=False, comment="是否隐藏主页")
    is_anonymous = Column(Boolean, default=False, comment="是否匿名")
    eat_tip = Column(Boolean, default=False, comment="是否被举报")
    crawled_at = Column(DateTime, default=datetime.utcnow, comment="抓取时间")
    fingerprint = Column(String(64), nullable=False, comment="用户指纹（SHA-256）")
    item_type = Column(String(10), default="user", comment="item 类型（post/user）")

