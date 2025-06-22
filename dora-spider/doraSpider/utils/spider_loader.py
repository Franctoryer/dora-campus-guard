from typing import Any

from scrapy.loader import ItemLoader


class PostItemLoader(ItemLoader):
    def load_item(self) -> Any:
        item = super().load_item()

        if "picture_urls" not in item:
            item["picture_urls"] = []
        if "ever_top_end_time" not in item:
            item["ever_top_end_time"] = None

        return item


class UserItemLoader(ItemLoader):
    def load_item(self) -> Any:
        item = super().load_item()

        if "avatar_url" not in item:
            item["avatar_url"] = None

        return item