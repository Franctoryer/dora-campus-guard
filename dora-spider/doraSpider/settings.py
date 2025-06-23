# Scrapy settings for doraSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.settings.default_settings import DOWNLOAD_DELAY

BOT_NAME = "doraSpider"

SPIDER_MODULES = ["doraSpider.spiders"]
NEWSPIDER_MODULE = "doraSpider.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "doraSpider (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 0.4

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "doraSpider.middlewares.DoraspiderSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "doraSpider.middlewares.DoraspiderDownloaderMiddleware": 543,
#}
DOWNLOADER_MIDDLEWARES = {
    # 'doraSpider.middlewares.RandomProxyMiddleware': 350,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,
}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "doraSpider.pipelines.LoggerPipeline": 200,
    # "doraSpider.pipelines.MySQLPipeline": 500,
    "doraSpider.pipelines.RabbitMQPipeline": 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = 'INFO'

# 数据库配置
MYSQL_DB_URL = 'mysql+pymysql://root:admin123@localhost:3306/dora?charset=utf8mb4'

# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]
RETRY_BACKOFF_BASE = 2
RETRY_BACKOFF_MAX = 30

# 代理
PROXY_USERNAME = "d2737415411"
PROXY_PASSWORD = "rrrz4u45"

PROXY_LIST = [
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@61.184.8.27:40476",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@36.151.192.236:40192",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@61.184.8.27:40297",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@182.106.136.217:40964",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@218.95.37.135:40638",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@36.151.192.236:40777",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@219.150.218.21:25950",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@58.19.55.8:25624",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@58.19.54.154:14551",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@58.19.55.9:34207",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@61.184.8.27:41499",
    f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@182.106.136.217:40879",
]

# RabbitMQ 配置
RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"

# 情感分析服务配置
SENTIMENT_HOST = "http://127.0.0.1:8000"
SENTIMENT_URL = "/predict-emotion"

# ES 配置
ES_URL = "http://localhost:9200"
ES_POST_INDEX = "posts"