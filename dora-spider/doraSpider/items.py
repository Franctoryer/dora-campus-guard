# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from email.quoprimime import body_length

import scrapy
from itemloaders import Identity
from itemloaders.processors import MapCompose, TakeFirst

from doraSpider.utils.time_util import TimeUtil


class PostItem(scrapy.Item):
    """
    帖子相关数据模型
    """
    # 帖子 ID
    id = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 帖子正文
    content = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # 发帖者 ID
    uid = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 是否匿名
    is_anonymous = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 是否精选
    is_distinguished = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 图片 url
    picture_urls = scrapy.Field(output_processor=Identity())
    # 是否有风险
    risky = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 话题 ID
    topic_id = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 评论数
    comment_sum = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 学校 id
    school_id = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # is_fee
    is_fee = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # origin
    origin = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # ad_level
    ad_level = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 是否已解决
    settled = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 点赞数
    like_sum = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 热度
    hot = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 举报数
    tip_sum = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 转发数
    forward_sum = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 蹲数
    dun_num = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 发布时间
    published_at = scrapy.Field(input_processor=MapCompose(TimeUtil.timestamp_to_datetime), output_processor=TakeFirst())
    # 是否曾经置顶
    is_ever_top = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 曾经置顶的结束时间
    ever_top_end_time = scrapy.Field(input_processor=MapCompose(TimeUtil.timestamp_to_datetime), output_processor=TakeFirst())
    # crawled_at
    crawled_at = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # 帖子指纹
    fingerprint = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # item 类型(post -- 帖子; user -- 用户)
    item_type = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())



class UserItem(scrapy.Item):
    """
    用户相关数据模型
    """
    # 用户 ID
    uid: int = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 用户头像
    avatar_url: str = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # 性别(0 女 1 男 2 保密)
    gender: int = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 等级
    level: int = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 昵称
    nickname: str = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # 是否是管理员
    is_admin: bool = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 学校 id
    school_id: float = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 哆啦币
    dora_coin: float = scrapy.Field(input_processor=MapCompose(float), output_processor=TakeFirst())
    # 是否隐藏了主页
    hide_permission: int = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 当前状态是否匿名
    is_anonymous: int = scrapy.Field(input_processor=MapCompose(int), output_processor=TakeFirst())
    # 是否被举报
    eat_tip: bool = scrapy.Field(input_processor=MapCompose(int, bool), output_processor=TakeFirst())
    # 抓取时间
    crawled_at: str = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # 用户指纹(sha256)
    fingerprint: str = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
    # item 类型(post -- 帖子; user -- 用户)
    item_type: str = scrapy.Field(input_processor=MapCompose(str), output_processor=TakeFirst())
