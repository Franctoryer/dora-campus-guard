import subprocess

# 启动爬虫
subprocess.run([
    "scrapy",
    "crawl",
    "postSpider"
])