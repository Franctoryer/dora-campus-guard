from datetime import datetime
from typing import Optional


class TimeUtil:
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> Optional[str]:
        """
        把时间戳转成 '%Y-%m-%d %H:%M:%S' 格式的字符串
        支持秒级（9位）和毫秒级（13位）时间戳
        :param timestamp: 时间戳
        :return: 时间字符串或 None
        """
        ts_str = str(timestamp)
        length = len(ts_str)
        if length == 10:
            # 10位秒级时间戳
            try:
                dt = datetime.fromtimestamp(int(timestamp))
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return None
        elif length == 13:
            # 13位毫秒级时间戳，先转成秒
            try:
                dt = datetime.fromtimestamp(int(timestamp) / 1000)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return None
        else:
            return None
