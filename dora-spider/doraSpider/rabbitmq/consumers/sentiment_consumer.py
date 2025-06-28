"""
情感分类消费者，做以下事情：
- 情感预测
- 存 MySQL
- 存 ES
"""
from datetime import datetime
import json
from typing import Dict, Any
import xmlrpc.client

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

            # 给 post 增加两个情感类型字段
            post["sentiment_label"] = emotion_label
            post["sentiment_confidence"] = emotion_confidence

            # 异常预警
            abnormal_index = self.get_abnormal_index(post["content"], emotion_label, post["tip_sum"])
            post["abnormal_index"] = abnormal_index

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
        # 情感分析服务 RPC 接口
        client = xmlrpc.client.ServerProxy(self.settings.get("SENTIMENT_RPC_HOST"))
        result: Dict[str, Any] = client.predict_emotion(text)  # 预测情感
        emotion_label = result["label_id"]
        emotion_confidence = result["confidence"]

        return emotion_label, emotion_confidence

    def get_abnormal_index(self, text: str, sentiment_label: int, tip_sum: int) -> int:
        """
        获取一个帖子的异常指数
        :param text: 文本
        :param sentiment_label: 情感类型
        :param tip_sum: 举报数
        :return:  1 -> 2 -> 3，异常指数逐渐升高
        """
        # 只有负面情感的帖子才会触发预警
        if sentiment_label != 0 and sentiment_label != 1 and sentiment_label != 2:
            return 0
        # 最后的异常指数
        result = 0
        # 异常预警 RPC 接口
        client = xmlrpc.client.ServerProxy(self.settings.get("DETECTION_RPC_HOST"))
        is_sensitive: bool = client.is_sensitive(text)

        # 如果含有敏感词 + 1
        if is_sensitive:
            result = result + 1

        if tip_sum > 0:
            result = result + 1

        if tip_sum >= 2:
            result = result + 1

        return result


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
            "abnormal_index": stmt.inserted.abnormal_index
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
                    "sentiment_confidence": post["sentiment_confidence"],
                    "abnormal_index": post["abnormal_index"],
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

    def update_all_sentiments_from_es(self, batch_size=1000):
        """
        遍历 ES 索引中的所有文档，预测内容的情感，更新 sentiment_label 和 sentiment_confidence 字段
        :param batch_size: 每次查询的批量大小，默认 1000
        """
        query = {
            "query": {"match_all": {}},
            "_source": ["content"],  # 只拉取 content 字段减少传输
            "size": batch_size,
        }

        scroll_id = None

        try:
            # 初始化scroll查询
            resp = self.es.search(index=self.es_post_index, body=query, scroll='2m')
            scroll_id = resp['_scroll_id']
            total = resp['hits']['total']['value']
            logger.info(f"开始更新 ES 中 {total} 条数据的情感")

            processed = 0
            while True:
                hits = resp['hits']['hits']
                if not hits:
                    break

                for hit in hits:
                    doc_id = hit['_id']
                    source = hit['_source']
                    content = source.get('content', '')
                    if not content:
                        continue

                    # 预测情感
                    label, confidence = self.predict_sentiment(content)

                    # 更新 ES 文档部分字段
                    self.es.update(
                        index=self.es_post_index,
                        id=doc_id,
                        body={
                            "doc": {
                                "sentiment_label": label,
                                "sentiment_confidence": confidence,
                            }
                        }
                    )
                    processed += 1

                logger.info(f"已处理 {processed}/{total} 条")

                # 继续scroll下一批
                resp = self.es.scroll(scroll_id=scroll_id, scroll='2m')

                # scroll结束条件
                if not resp['hits']['hits']:
                    break

            logger.success(f"完成情感更新，共处理 {processed} 条数据")
        except Exception as e:
            logger.error(f"更新 ES 情感字段失败: {e}")
        finally:
            if scroll_id:
                try:
                    self.es.clear_scroll(scroll_id=scroll_id)
                except Exception:
                    pass

    def update_all_sentiment_from_mysql(self, batch_size=1000):
        """
        遍历 MySQL 中 sentiment_label 为空的帖子，调用情感模型进行预测，并更新 sentiment_label 和 sentiment_confidence 字段。
        :param batch_size: 每批处理的数量
        """
        try:
            offset = 0
            processed = 0

            while True:
                # 查询 sentiment_label 为空的帖子
                posts = (
                    self.session.query(Post)
                    .filter(Post.sentiment_label == None)
                    .order_by(Post.id)
                    .offset(offset)
                    .limit(batch_size)
                    .all()
                )

                if not posts:
                    break

                for post in posts:
                    if not post.content:
                        continue

                    # 调用情感分析模型
                    label, confidence = self.predict_sentiment(post.content)

                    # 更新字段
                    post.sentiment_label = label
                    post.sentiment_confidence = confidence

                    processed += 1

                self.session.commit()
                logger.info(f"已处理 {processed} 条")

                if len(posts) < batch_size:
                    break  # 数据处理完了

                offset += batch_size

            logger.success(f"MySQL 情感字段更新完成，共处理 {processed} 条")
        except Exception as e:
            self.session.rollback()
            logger.error(f"更新 MySQL 情感字段失败: {e}")


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
    # consumer = SentimentConsumer()
    # consumer.update_all_sentiment_from_mysql()
