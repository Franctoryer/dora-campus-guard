import hashlib
import json
from datetime import timezone, timedelta, datetime
from typing import AsyncIterator, Any, Dict, List
from urllib.parse import urlencode

import scrapy
from fake_useragent import UserAgent
from jsonpath import jsonpath
from loguru import logger
from scrapy import Request
from scrapy.http import Response
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TCPTimedOutError

from doraSpider.configs.spider_config import post_list_config, post_detail_config, user_info_config
from doraSpider.items import PostItem, UserItem
from doraSpider.utils.cipher import AESCipher
from doraSpider.utils.spider_loader import PostItemLoader, UserItemLoader


class SufePostSpiderSpider(scrapy.Spider):
    """
    该爬虫只爬取上财校圈的数据，链式访问列表页
    """
    name = "sufe_post_spider"
    allowed_domains = ["dolacc.com"]
    start_urls = ["https://dolacc.com"]

    # UA 对象 (用于随机生成客户代理)
    ua = UserAgent()
    default_headers = {
        'xweb_xhr': '1',
        'Content-Type': 'application/json; charset=UTF-8',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://servicewechat.com/wx9ddd73d26fdbacba/374/page-frame.html',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def __init__(self, page_num: int = 100, first_index: int = -1, *args, **kwargs):
        """
        初始化函数
        :param page_num: 抓取页数
        :param first_index: 第一个帖子 ID，-1 表示最新
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.page_num = int(page_num)
        self.first_index = int(first_index)

    async def start(self) -> AsyncIterator[Any]:
        post_list_url: str = "https://cdn.dolacc.com/index.php/api/Wxpostv2/getPostsCdnpw"
        post_list_start_params = {
            "toId": "0",
            "scId": "16",
            "pageSize": "10",
            "lastindex": f"{self.first_index}",
            "keyword": "",
            "freshKey": "0"
        }
        # 拼接 url
        query_string = urlencode(post_list_start_params)
        full_url = f"{post_list_url}?{query_string}"

        yield Request(
            url=full_url,
            headers={
                **self.default_headers,
                'User-Agent': self.ua.random
            },
            cb_kwargs={
                "current_page": 1
            },
            callback=self.parse_index,
        )

    def parse_index(self, response: Response, **kwargs):
        # 获取帖子 ID 配置
        id_config = post_list_config["fields"][0]
        id_jsonpath = id_config["path"]

        # 解析帖子 ID
        post_json = json.loads(response.text)
        post_ids = jsonpath(post_json, id_jsonpath)

        for post_id in post_ids:
            url = f"https://cdn.dolacc.com/index.php/api/wxPostv2/visitPostCdnPw?pId={post_id}&nocache=-1"
            # 发请求

            yield Request(
                url=url,
                headers={
                    **self.default_headers,
                    'User-Agent': self.ua.random
                },
                callback=self.parse_post_detail,
                errback=self.handle_error,
                meta={
                    "post_id": post_id
                },
                dont_filter=True
            )

        # ------------- 下一页请求 ---------------
        # 获取当前页码
        current_page = kwargs.get("current_page")
        if current_page > self.page_num:
            return
        last_id = post_ids[-1]
        post_list_url: str = "https://cdn.dolacc.com/index.php/api/Wxpostv2/getPostsCdnpw"
        post_list_start_params = {
            "toId": "0",
            "scId": "16",
            "pageSize": "10",
            "lastindex": f"{last_id}",
            "keyword": "",
            "freshKey": "0"
        }
        # 拼接 url
        query_string = urlencode(post_list_start_params)
        full_url = f"{post_list_url}?{query_string}"

        yield Request(
            url=full_url,
            headers={
                **self.default_headers,
                'User-Agent': self.ua.random
            },
            cb_kwargs={
                "current_page": current_page + 1
            },
            callback=self.parse_index,
        )



    def parse_post_detail(self, response: Response):
        """
        解析详情页
        :param response:
        :return:
        """
        post_id = response.meta.get('post_id', 'unknown')
        logger.info(f"Received response for post ID: {post_id}, status: {response.status}")
        # 帖子数据
        yield PostItem(self.create_post_items(response))
        # 用户数据
        yield UserItem(self.create_user_items(response))

    def create_post_items(self, response: Response) -> Dict[str, Any]:
        """
        构建帖子 item
        :param response:
        :return:
        """
        # 解析列表页数据
        posts_json = json.loads(response.text)

        # 帖子数据
        loader = PostItemLoader(item=PostItem())

        # 获取字段配置
        fields = post_detail_config["fields"]
        for field in fields:
            try:
                field_name = field["name"]
                field_path = field["path"]
                field_value = jsonpath(posts_json, field_path)[0]
                loader.add_value(field_name, field_value)
            except Exception as e:
                self.logger.warning(f"字段 {field_name} 解析失败: {e}")
        # 帖子后处理
        post_item = loader.load_item()
        self.out_process_post_item(post_item)

        return post_item

    def create_user_items(self, response: Response) -> Dict[str, Any]:
        """
        构建用户 item
        :param response:
        :return:
        """
        # 解析列表页数据
        posts_json = json.loads(response.text)

        # 用户数据
        loader = UserItemLoader(item=UserItem())

        # 获取字段配置
        fields = user_info_config["fields"]
        for field in fields:
            field_name = field["name"]
            field_path = field["path"]
            field_value = jsonpath(posts_json, field_path)[0]
            loader.add_value(field_name, field_value)

        user_item = loader.load_item()
        self.out_process_user_item(user_item)

        return user_item

    def handle_error(self, failure):
        self.logger.error(repr(failure))  # 输出错误信息

        # 分类型处理
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error(f"HTTP 错误 {response.status} on {response.url}")

        elif failure.check(DNSLookupError):
            request = failure.request
            self.logger.error(f"DNS 查询失败: {request.url}")

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error(f"请求超时: {request.url}")

        elif failure.check(ConnectionRefusedError):
            request = failure.request
            self.logger.error(f"连接被拒绝: {request.url}")

        else:
            request = failure.request
            self.logger.error(f"未知错误: {request.url}")

    @staticmethod
    def merge_item(item_map: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
        """
        把 {key1: [...], key2: [...], key3: [...]} 转换成
        [{key1: val1, key2: val2, key3: val3}, ...]
        :param item_map: 字典，每个键对应一个值列表
        :return: 合并后的列表，每个元素是一个字典
        """
        keys = list(item_map.keys())
        values_lists = list(item_map.values())

        # 保证所有 value 列表长度一致
        if not values_lists:
            return []

        length = len(values_lists[0])
        if not all(len(lst) == length for lst in values_lists):
            raise ValueError("All value lists must be of the same length")

        merged = []
        for i in range(length):
            merged.append({key: item_map[key][i] for key in keys})

        return merged

    @staticmethod
    def decrypt_post_content(ciphertext_base64: str) -> str:
        """
        帖子正文进行了 AES 解密
        :param ciphertext_base64: 密文
        :return:
        """
        return AESCipher.aes_cbc_decrypt(
            key="IVIVIV_LUYILAFEI",
            iv="XDXDXU_LUYILAFEI",
            cipher_text=ciphertext_base64
        )

    def out_process_post_item(self, post_item: Dict[str, Any]):
        """
        帖子 item 后处理
        :param post_item:
        :return:
        """
        # 帖子正文解密
        post_item["content"] = self.decrypt_post_content(post_item["content"])

        # 将 url 列表转化成字符串
        if isinstance(post_item["picture_urls"], list):
            post_item["picture_urls"] = ",".join(post_item["picture_urls"])

        # 抓取时间
        tz = timezone(timedelta(hours=8))
        post_item["crawled_at"] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')

        # 计算数据指纹
        fingerprint_fields = {
            "id": post_item["id"],
            "content": post_item["content"],
            "comment_sum": post_item["comment_sum"],
            "like_sum": post_item["like_sum"],
            "hot": post_item["hot"],
            "tip_sum": post_item["tip_sum"],
            "forward_sum": post_item["forward_sum"],
            "dun_num": post_item["dun_num"],
        }
        fingerprint = self.get_fingerprint(json.dumps(fingerprint_fields, ensure_ascii=False, sort_keys=True))
        post_item["fingerprint"] = fingerprint

        # item 类型
        post_item["item_type"] = "post"

    def out_process_user_item(self, user_item: Dict[str, Any]):
        """
        用户数据后处理
        :param user_item:
        :return:
        """
        # 抓取时间
        tz = timezone(timedelta(hours=8))
        user_item["crawled_at"] = datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')

        # 数据指纹
        fingerprint_fields = {
            "uid": user_item["uid"],
            "avatar_url": user_item["uid"],
            "gender": user_item["gender"],
            "level": user_item["level"],
            "nickname": user_item["nickname"],
            "dora_coin": user_item["dora_coin"],
            "hide_permission": user_item["hide_permission"],
        }
        fingerprint = self.get_fingerprint(json.dumps(fingerprint_fields, ensure_ascii=False, sort_keys=True))
        user_item["fingerprint"] = fingerprint

        # item 类型
        user_item["item_type"] = "user"

    @staticmethod
    def get_fingerprint(data: str) -> str:
            """
            用 sha256 哈希计算数据指纹
            :param data:
            :return:
            """
            sha256 = hashlib.sha256()
            sha256.update(data.encode('utf-8'))  # 将字符串编码为 bytes
            return sha256.hexdigest()
