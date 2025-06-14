# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PostItem(scrapy.Item):
    """
    帖子相关数据模型
    """
    # 帖子 ID
    id = scrapy.Field()
    # 帖子正文
    content = scrapy.Field()
    # 发帖者 ID
    uid = scrapy.Field()
    # 是否匿名
    is_anonymous = scrapy.Field()
    # 是否精选
    is_distinguished = scrapy.Field()
    # 图片 url
    picture_urls = scrapy.Field()
    # 话题 ID
    topic_id = scrapy.Field()
    # 评论数
    comment_sum = scrapy.Field()
    # 点赞数
    like_sum = scrapy.Field()
    # 热度
    hot = scrapy.Field()
    # 举报数
    tip_sum = scrapy.Field()
    # 转发数
    forward_sum = scrapy.Field()
    # 发布时间
    published_at = scrapy.Field()
    # 是否曾经置顶
    is_ever_top = scrapy.Field()
    # 曾经置顶的结束时间
    ever_top_end_time = scrapy.Field()
    # item 类型(post -- 帖子; user -- 用户)
    item_type = scrapy.Field()



class UserItem(scrapy.Item):
    """
    用户相关数据模型
    """
    # 用户 ID
    uid = scrapy.Field()
    # 用户头像
    avatar_url = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 等级
    level = scrapy.Field()
    # 昵称
    nickname = scrapy.Field()
    # 是否是管理员
    is_admin = scrapy.Field()
    # 哆啦值
    dora_value = scrapy.Field()
    # 哆啦币
    dora_coin = scrapy.Field()
    # 被那些人关注？(暂时未知)
    likes = scrapy.Field()
    # 是否隐藏了主页
    hide_permission = scrapy.Field()
    # 当前状态是否匿名
    is_anonymous = scrapy.Field()
    # item 类型(post -- 帖子; user -- 用户)
    item_type = scrapy.Field()
