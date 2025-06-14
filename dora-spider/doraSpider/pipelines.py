# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from typing import Optional

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from doraSpider.items import PostItem, UserItem
from loguru import logger
from datetime import datetime


class LoggerPipeline:
    # 累计爬取的帖子数
    post_accumulation = 0
    # 累计爬取的用户数
    user_accumulation = 0


    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_type = adapter.get("item_type")
        if item_type == "post":
            return self.process_post_item(item, spider)
        elif item_type == "user":
            return self.process_user_item(item, spider)
        else:
            return item

    def process_post_item(self, item: PostItem, spider):
        logger.info(f"用户 {item['uid']} 发帖：{item['content'][:20]} ...".replace("\n", ""))
        self.post_accumulation = self.post_accumulation + 1
        if self.post_accumulation % 100 == 0:
            logger.success(f"------------ 已累计爬取 {self.post_accumulation} 条帖子 ------------\n")
        return item

    def process_user_item(self, item: UserItem, spider):
        logger.info(f"用户 {item['uid']} {item['nickname']}")
        self.user_accumulation = self.user_accumulation + 1
        if self.user_accumulation % 100 == 0:
            logger.success(f"------------ 已累计爬取 {self.user_accumulation} 条用户信息 ------------\n")

        return item



class PostPipline:
    # 帖子数据
    post_batch = []
    # 用户数据
    user_batch = []
    # 批量处理大小
    batch_size = 100

    def __init__(self, host: str, port: int, user: str, password, db: str, charset: str) -> None:
        """
        初始化函数
        :param host: 主机名称
        :param port: 数据库端口
        :param user: 数据库用户
        :param password: 密码
        :param db: 数据库名称
        :param charset: 字符编码格式（utf8mb4）
        """
        self.cursor = None
        self.conn = None
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.getint('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            db=crawler.settings.get('MYSQL_DATABASE'),
            charset=crawler.settings.get('MYSQL_CHARSET', 'utf8mb4')
        )

    def open_spider(self, spider):
        """
        建立数据库连接
        :param spider:
        :return:
        """
        self.conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db,
            charset=self.charset
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        """
        关闭数据库连接
        :param spider:
        :return:
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_post_item(self, item, spider):
        adapter = ItemAdapter(item)
        sql = """
            INSERT INTO posts (
                id, content, uid, is_anonymous, is_distinguished, picture_urls,
                topic_id, comment_sum, like_sum, hot, tip_sum, forward_sum,
                published_at, is_ever_top, ever_top_end_time, update_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            ON DUPLICATE KEY UPDATE 
                content=VALUES(content),
                like_sum=VALUES(like_sum),
                comment_sum=VALUES(comment_sum),
                hot=VALUES(hot),
                tip_sum=VALUES(tip_sum),
                forward_sum=VALUES(forward_sum),
                is_ever_top = IF(VALUES(is_ever_top) = 1, VALUES(is_ever_top), is_ever_top),
                ever_top_end_time = IF(VALUES(is_ever_top) = 1, VALUES(ever_top_end_time), ever_top_end_time),
                update_time = NOW()
        """

        values = (
            adapter.get('id'),
            adapter.get('content'),
            adapter.get('uid'),
            adapter.get('is_anonymous'),
            adapter.get('is_distinguished'),
            adapter.get('picture_urls'),
            adapter.get('topic_id'),
            adapter.get('comment_sum'),
            adapter.get('like_sum'),
            adapter.get('hot'),
            adapter.get('tip_sum'),
            adapter.get('forward_sum'),
            self.timestamp_to_datetime(adapter.get('published_at')),
            adapter.get('is_ever_top'),
            self.timestamp_to_datetime(adapter.get('ever_top_end_time')),
        )
        # 放入缓冲区
        self.post_batch.append(values)
        # 如果 < batch_size 直接返回
        if len(self.post_batch) < self.batch_size:
            return item

        # 否则，插入数据库
        try:
            # 批量插入
            self.cursor.executemany(sql, self.post_batch)
            self.conn.commit()
            # 清空缓冲区
            self.post_batch = []
        except pymysql.MySQLError as e:
            spider.logger.error(f"MySQL 插入失败: {e}")

        return item

    def process_user_item(self, item, spider):
        adapter = ItemAdapter(item)
        sql="""
            INSERT INTO users (
                uid, avatar_url, gender, level, nickname, is_admin, 
                dora_value, dora_coin, likes, hide_permission, 
                is_anonymous, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW()
            ) ON DUPLICATE KEY UPDATE
                avatar_url = VALUES(avatar_url) IF(VALUES(is_anonymous) = 0, VALUES(avatar_url), avatar_url),
                gender = VALUES(gender) IF(VALUES(is_anonymous) = 0, VALUES(gender), gender),
                level = VALUES(level),
                nickname = IF(VALUES(is_anonymous) = 0, VALUES(nickname), nickname),
                is_admin = VALUES(is_admin),
                dora_value = VALUES(dora_value),
                dora_coin = VALUES(dora_coin),
                likes = VALUES(likes),
                hide_permission = VALUES(hide_permission),
                is_anonymous = IF(VALUES(is_anonymous) = 0, VALUES(is_anonymous), is_anonymous)
        """
        values = (
            adapter.get('uid'),
            adapter.get('avatar_url'),
            adapter.get('gender', 2),
            adapter.get('level'),
            adapter.get('nickname'),
            adapter.get('is_admin', False),
            adapter.get('dora_value', 0.0),
            adapter.get('dora_coin', 0.0),
            adapter.get('likes'),
            adapter.get('hide_permission', False),
            adapter.get('is_anonymous', False),
            self.timestamp_to_datetime(adapter.get('created_at'))
        )
        # 放入缓冲区
        self.user_batch.append(values)
        # 如果 < batch_size 直接返回
        if len(self.user_batch) < self.batch_size:
            return item

        # 否则，插入数据库
        try:
            # 批量插入
            self.cursor.executemany(sql, self.user_batch)
            self.conn.commit()
            # 清空缓冲区
            self.user_batch = []
        except pymysql.MySQLError as e:
            spider.logger.error(f"MySQL 插入失败: {e}")

        return item

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item_type = adapter.get("item_type")
        if item_type == "post":
            return self.process_post_item(item, spider)
        elif item_type == "user":
            return self.process_user_item(item, spider)
        else:
            return item

    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> Optional[str]:
        """
        把时间戳转成 '%Y-%m-%d %H:%M:%S' 格式的字符串
        支持秒级（9位）和毫秒级（13位）时间戳
        :param timestamp: 时间戳
        :return: 时间字符串或 None
        """
        ts_str = str(timestamp)
        length = len(ts_str)
        if length == 10:
            # 10位秒级时间戳
            try:
                dt = datetime.fromtimestamp(int(timestamp))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return None
        elif length == 13:
            # 13位毫秒级时间戳，先转成秒
            try:
                dt = datetime.fromtimestamp(int(timestamp) / 1000)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return None
        else:
            return None