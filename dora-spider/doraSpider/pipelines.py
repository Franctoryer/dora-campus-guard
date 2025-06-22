# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from typing import Optional, Any, List

import pymysql
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from doraSpider.items import PostItem, UserItem
from loguru import logger


from doraSpider.models import Base, Post, User
from sqlalchemy import create_engine, func, case
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert as mysql_insert



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
        self.post_accumulation = self.post_accumulation + 1
        # logger.info(f"{item['id']} | {item['content']} | {item['uid']}")
        if self.post_accumulation % 1000 == 0:
            logger.success(f"------------ 已累计爬取 {self.post_accumulation} 条帖子 ------------\n")
            logger.success(f"当前帖子 ID: {item['id']}")
        return item

    def process_user_item(self, item: UserItem, spider):
        self.user_accumulation = self.user_accumulation + 1
        if self.user_accumulation % 1000 == 0:
            logger.success(f"------------ 已累计爬取 {self.user_accumulation} 条用户信息 ------------\n")

        return item



class MySQLBatchPipeline:
    def __init__(self, db_url, batch_size=500):
        self.db_url = db_url
        self.batch_size = batch_size
        # 帖子数据
        self.post_batch = []
        # 用户数据
        self.user_batch = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=crawler.settings.get("MYSQL_DB_URL"),
            batch_size=crawler.settings.getint("BATCH_SIZE", 500)
        )

    def open_spider(self, spider):
        engine = create_engine(self.db_url)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

        logger.success("数据库连接成功！")

    def close_spider(self, spider):
        # 清理剩余数据
        self.flush_batch()
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        data = adapter.asdict()

        # 根据 item_type 判断插入哪个表
        item_type = data.get("item_type")
        if item_type == "post":
            self.post_batch.append(data)
        elif item_type == "user":
            self.user_batch.append(data)
        else:
            spider.logger.warning(f"未知 item_type: {item_type}")
            return item

        # 批量更新帖子
        if len(self.post_batch) >= self.batch_size:
            self.bulk_upsert_post(self.post_batch)
            self.post_batch = []

        # 批量更新用户
        if len(self.user_batch) >= self.batch_size:
            self.bulk_upsert_user(self.user_batch)
            self.user_batch = []

        return item

    def bulk_upsert_user(self, items: List[Any]):
        """
        批量插入或更新用户数据
        :param items:
        :return:
        """
        table = User.__table__
        stmt = mysql_insert(table).values(items)

        update_dict = {
            "nickname": case(
                (table.c.is_anonymous == True, stmt.inserted.nickname),
                else_=table.c.nickname
            ),
            "avatar_url": case(
                (table.c.is_anonymous == True, stmt.inserted.avatar_url),
                else_=table.c.avatar_url
            ),
            "level": stmt.inserted.level,
            "gender": stmt.inserted.gender,
            "dora_coin": stmt.inserted.dora_coin,
            "hide_permission": stmt.inserted.hide_permission,
            "eat_tip": stmt.inserted.eat_tip,
            "is_anonymous": stmt.inserted.is_anonymous,
        }
        on_duplicate_key_stmt = stmt.on_duplicate_key_update(**update_dict)

        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            print(f"User 批量 upsert 成功，数量: {len(items)}")
        except Exception as e:
            self.session.rollback()
            print(f"User 批量 upsert 失败: {e}")


    def bulk_upsert_post(self, items: List[Any]):
        """
        批量插入或更新用户数据
        :param items:
        :return:
        """
        table = Post.__table__
        stmt = mysql_insert(table).values(items)

        update_dict = {
            "is_distinguished": stmt.inserted.is_distinguished,
            "risky": stmt.inserted.risky,
            "comment_sum": stmt.inserted.comment_sum,
            "like_sum": stmt.inserted.like_sum,
            "hot": stmt.inserted.hot,
            "tip_sum": stmt.inserted.tip_sum,
            "forward_sum": stmt.inserted.forward_sum,
            "is_fee": stmt.inserted.is_fee,
            "settled": stmt.inserted.settled,
            "is_ever_top": stmt.inserted.is_ever_top,
            "ever_top_end_time": stmt.inserted.ever_top_end_time,
        }
        on_duplicate_key_stmt = stmt.on_duplicate_key_update(**update_dict)

        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            print(f"Post 批量 upsert 成功，数量: {len(items)}")
        except Exception as e:
            self.session.rollback()
            print(f"Post 批量 upsert 失败: {e}")

    def flush_batch(self):
        self.bulk_upsert_post(self.post_batch)
        self.bulk_upsert_user(self.user_batch)


class MySQLPipeline:
    def __init__(self, db_url):
        self.db_url = db_url

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=crawler.settings.get("MYSQL_DB_URL"),
        )

    def open_spider(self, spider):
        from sqlalchemy import create_engine
        engine = create_engine(self.db_url)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

        logger.success("数据库连接成功！")

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        data = adapter.asdict()

        item_type = data.get("item_type")
        if item_type == "post":
            self.upsert_post(data)
        elif item_type == "user":
            self.upsert_user(data)
        else:
            spider.logger.warning(f"未知 item_type: {item_type}")
        return item

    def upsert_user(self, item: Any):
        table = User.__table__
        stmt = mysql_insert(table).values(**item)

        update_dict = {
            "nickname": case(
                (table.c.is_anonymous == True, stmt.inserted.nickname),
                else_=table.c.nickname
            ),
            "avatar_url": case(
                (table.c.is_anonymous == True, stmt.inserted.avatar_url),
                else_=table.c.avatar_url
            ),
            "level": stmt.inserted.level,
            "gender": stmt.inserted.gender,
            "dora_coin": stmt.inserted.dora_coin,
            "hide_permission": stmt.inserted.hide_permission,
            "eat_tip": stmt.inserted.eat_tip,
            "is_anonymous": stmt.inserted.is_anonymous,
        }

        on_duplicate_key_stmt = stmt.on_duplicate_key_update(**update_dict)

        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            logger.debug(f"User upsert 成功: {item.get('id')}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"User upsert 失败: {e}")

    def upsert_post(self, item: Any):
        table = Post.__table__
        stmt = mysql_insert(table).values(**item)

        update_dict = {
            "is_distinguished": stmt.inserted.is_distinguished,
            "risky": stmt.inserted.risky,
            "comment_sum": stmt.inserted.comment_sum,
            "like_sum": stmt.inserted.like_sum,
            "hot": stmt.inserted.hot,
            "tip_sum": stmt.inserted.tip_sum,
            "forward_sum": stmt.inserted.forward_sum,
            "is_fee": stmt.inserted.is_fee,
            "settled": stmt.inserted.settled,
            "is_ever_top": stmt.inserted.is_ever_top,
            "ever_top_end_time": stmt.inserted.ever_top_end_time,
        }

        on_duplicate_key_stmt = stmt.on_duplicate_key_update(**update_dict)

        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            logger.debug(f"Post upsert 成功: {item.get('id')}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Post upsert 失败: {e}")