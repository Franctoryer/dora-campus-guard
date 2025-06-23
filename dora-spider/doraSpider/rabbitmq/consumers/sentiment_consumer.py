"""
情感分类消费者，做以下事情：
- 情感预测
- 存 MySQL
- 存 ES
"""
from datetime import datetime
import json
from typing import Dict, Any

import pika
import requests
from elasticsearch import Elasticsearch
from loguru import logger
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert as mysql_insert

from doraSpider.models import Base, Post


class SentimentConsumer:
    """
    情感分析消费者
    """

    def __init__(self):
        # 读取配置
        self.settings = get_project_settings()
        # 数据库 url
        self.mysql_db_url = self.settings.get("MYSQL_DB_URL")
        # Rabbitmq URL
        self.rabbitmq_url = self.settings.get("RABBITMQ_URL")
        # ElasticSearch URL
        self.es_url = self.settings.get("ES_URL")
        self.es_post_index = self.settings.get("ES_POST_INDEX")

        # MySQL 连接
        engine = create_engine(self.mysql_db_url)
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        logger.info("MySQL 连接成功")

        # ES 连接
        self.es = Elasticsearch(self.es_url)

    def callback(self, ch, method, properties, body):
        """
        消费者回调函数
        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        """
        try:
            # 解析帖子数据
            post = json.loads(body)
            item_type = post.get("item_type")
            if item_type != "post":
                return
            logger.info(f"[X]: 接受消息: {post}")
            content = post.get("content")
            emotion_label, emotion_confidence = self.predict_sentiment(content)

            # 给 post 增加两个字段
            post["sentiment_label"] = emotion_label
            post["sentiment_confidence"] = emotion_confidence

            # 存到 MySQL
            self.mysql_upsert_post(post)

            # 存到 ES
            self.es_upsert_post(post)

            logger.success(f"MySQL & ES 插入成功 : {post}")

            # 消息确认
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(f"消息处理失败: {e}")
            # 重新入队
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def predict_sentiment(self, text: str) -> tuple[Any, Any]:
        """
        预测情感类型和置信度
        :param text:
        :return:
        """
        sentiment_host = self.settings.get("SENTIMENT_HOST")
        sentiment_url = self.settings.get("SENTIMENT_URL")

        json_data = {
            "text": text
        }
        resp = requests.post(f"{sentiment_host}{sentiment_url}", json=json_data)
        resp_json = resp.json()
        emotion_label = resp_json["label_id"]
        emotion_confidence = resp_json["confidence"]

        return emotion_label, emotion_confidence

    def mysql_upsert_post(self, item: Any):
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
            "sentiment_label": stmt.inserted.sentiment_label,
            "sentiment_confidence": stmt.inserted.sentiment_confidence,
        }

        on_duplicate_key_stmt = stmt.on_duplicate_key_update(**update_dict)

        try:
            self.session.execute(on_duplicate_key_stmt)
            self.session.commit()
            logger.debug(f"Post upsert 成功: {item.get('id')}")
        except Exception as e:
            self.session.rollback()
            logger.error(f"Post upsert 失败: {e}")

    def es_upsert_post(self, post: Any):
        self.es.update(
            index=self.es_post_index,
            id=post["id"],
            body={
                "doc": {
                    "id": post["id"],
                    "content": post["content"],
                    "uid": post["uid"],
                    "is_anonymous": post["is_anonymous"],
                    "is_distinguished": post["is_distinguished"],
                    "risky": post["risky"],
                    "topic_id": post["topic_id"],
                    "comment_sum": post["comment_sum"],
                    "like_sum": post["like_sum"],
                    "hot": post["hot"],
                    "tip_sum": post["tip_sum"],
                    "forward_sum": post["forward_sum"],
                    "dun_num": post["dun_num"],
                    "school_id": post["school_id"],
                    "settled": post["settled"],
                    "published_at":  self.normalize_datetime_str(post["published_at"]),
                    "sentiment_label": post["sentiment_label"],
                    "is_ever_top": post["is_ever_top"],
                    "ever_top_end_time": self.normalize_datetime_str(post["ever_top_end_time"]),
                },
                "doc_as_upsert": True
            }
        )

    @staticmethod
    def normalize_datetime_str(date_str: str | None) -> str | None:
        """
        日期正则化
        :param date_str:
        :return:
        """
        if not date_str:
            return None
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return dt.isoformat()
        except Exception:
            return date_str

def main() -> None:
    consumer = SentimentConsumer()
    conn = pika.BlockingConnection(pika.URLParameters(consumer.rabbitmq_url))
    channel = conn.channel()
    channel.queue_declare(queue='sentiment_tasks', durable=True)
    # channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sentiment_tasks', on_message_callback=consumer.callback)

    # 消费数据
    logger.info("[X]: 等待消息")
    channel.start_consuming()

if __name__ == '__main__':
    main()