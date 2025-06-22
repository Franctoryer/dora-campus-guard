import os
from scrapy.cmdline import execute

# 爬虫名称
spider_name = "postSpider"

# 可选参数
data_size = 1000000
first_index = -1

# 构造命令
cmd = f"scrapy crawl {spider_name} -a data_size={data_size} -a first_index={first_index}"

# 执行命令
execute(cmd.split())
