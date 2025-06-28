import os
import subprocess
from scrapy.cmdline import execute
from loguru import logger

# ---------- 启动消费者 -----------
consumer_process = subprocess.Popen(["uv", "run", "python", "./doraSpider/rabbitmq/consumers/sentiment_consumer.py"])
logger.success("消费者启动成功")

# ---------- 启动爬虫 ---------------
# spider_name = "postSpider"
# data_size = 1000000
# first_index = -1
# cmd = f"scrapy crawl {spider_name} -a data_size={data_size} -a first_index={first_index}"

spider_name = "sufe_post_spider"
page_num = 100000
first_index = 3071354
cmd = f"scrapy crawl {spider_name} -a page_num={page_num} -a first_index={first_index}"


# 执行命令
execute(cmd.split())
