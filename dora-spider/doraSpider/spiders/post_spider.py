import json
from typing import Iterable, Any, Optional, List

import scrapy
from jsonpath import jsonpath
from scrapy import Request
from scrapy.http import Response
from urllib.parse import urlencode
from fake_useragent import UserAgent
from loguru import logger
from typing import Dict, Any

from doraSpider.configs.spider_config import post_spider_config, user_spider_config
from doraSpider.items import PostItem, UserItem
from doraSpider.utils.cipher import AESCipher


class PostSpider(scrapy.Spider):
    name = "postSpider"
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
    # 爬取页数
    page_num = 1000000000

    def start_requests(self) -> Iterable[Any]:
        """
        列表页请求
        :return:
        """
        POST_LIST_URL: str = "https://cdn.dolacc.com/index.php/api/Wxpostv2/getPostsCdnpw"
        POST_LIST_START_PARAMS = {
            "toId": "0",
            "scId": "16",
            "pageSize": "10",
            "lastindex": "-1",
            "keyword": "",
            "freshKey": "0"
        }
        # 拼接 url
        query_string = urlencode(POST_LIST_START_PARAMS)
        full_url = f"{POST_LIST_URL}?{query_string}"

        yield Request(
            url=full_url,
            headers={
                **self.default_headers,
                'User-Agent': self.ua.random
            },
            callback=self.parse_list,
            cb_kwargs={
                "acc": 1
            }
        )

    def parse_list(self, response: Response, **kwargs: Dict[str, Any]):
        """
        解析列表页
        :param response:
        :param kwargs:
        :return:
        """
        # 获取已有的请求累计数
        acc = kwargs.get("acc", -1)
        # 若超出页数直接返回
        if acc > self.page_num:
            return

        # 帖子数据
        post_items = self.create_post_items(response)
        post_items = [PostItem(**item, item_type="post") for item in post_items]

        # 用户数据
        user_items = self.create_user_items(response)
        user_items = [UserItem(**item, item_type="user") for item in user_items]

        yield from post_items
        yield from user_items

        # 获取最后一个帖子的 ID，继续发请求
        last_index = post_items[-1]["id"]
        POST_LIST_URL: str = "https://cdn.dolacc.com/index.php/api/Wxpostv2/getPostsCdnpw"
        POST_LIST_START_PARAMS = {
            "toId": "0",
            "scId": "16",
            "pageSize": "10",
            "lastindex": f"{last_index}",
            "keyword": "",
            "freshKey": "0"
        }
        # 拼接 url
        query_string = urlencode(POST_LIST_START_PARAMS)
        full_url = f"{POST_LIST_URL}?{query_string}"

        yield Request(
            url=full_url,
            headers={
                **self.default_headers,
                'User-Agent': self.ua.random
            },
            callback=self.parse_list,
            cb_kwargs={
                "acc": acc + 1
            }
        )


    def create_post_items(self, response: Response) -> List[Dict[str, Any]]:
        """
        构建帖子 item
        :param response:
        :return:
        """
        # 解析列表页数据
        posts_json = json.loads(response.text)

        # 帖子数据
        post_items = {}

        # 获取字段配置
        fields = post_spider_config["fields"]
        for field in fields:
            field_name = field["name"]
            field_path = field["path"]
            field_value = jsonpath(posts_json, field_path)
            post_items[field_name] = field_value

        post_items = self.merge_item(post_items)

        # 帖子正文需要解密
        for post_item in post_items:
            post_item["content"] = self.decrypt_post_content(post_item["content"])

        return post_items

    def create_user_items(self, response: Response) -> List[Dict[str, Any]]:
        """
        构建用户 item
        :param response:
        :return:
        """
        # 解析列表页数据
        posts_json = json.loads(response.text)

        # 用户数据
        user_items = {}

        # 获取字段配置
        fields = user_spider_config["fields"]
        for field in fields:
            field_name = field["name"]
            field_path = field["path"]
            field_value = jsonpath(posts_json, field_path)
            user_items[field_name] = field_value

        user_items = self.merge_item(user_items)

        return user_items


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


