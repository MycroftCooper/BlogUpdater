import math
from datetime import datetime
from PyQt5.QtCore import QDateTime


class FormatHelper:
    time_str_format = '%Y-%m-%d %H:%M:%S'

    @staticmethod
    def qt_time_2_int_timestamp(qdt: QDateTime):
        pydt = qdt.toPyDateTime()
        formatted_date_str = pydt.strftime(FormatHelper.time_str_format)
        dt = datetime.strptime(formatted_date_str, FormatHelper.time_str_format)
        int_timestamp = int(dt.timestamp())
        return int_timestamp

    @staticmethod
    def int_timestamp_2_qt_time(int_timestamp: int):
        qdt = QDateTime.fromSecsSinceEpoch(int_timestamp)
        return qdt

    @staticmethod
    def int_timestamp_2_str(timestamp):
        return datetime.fromtimestamp(timestamp).strftime(FormatHelper.time_str_format)

    @staticmethod
    def str_data_2_list_data(str_data: str, split: str):
        stripped_items = [item_str.strip() for item_str in str_data.split(split) if item_str.strip()]
        result = sorted(set(stripped_items))
        return result

    @staticmethod
    def list_data_2_str_data(list_data: list, split: str):
        filtered_list_data = [item.strip() for item in list_data if item and item.strip()]
        str_data = split.join(sorted(set(filtered_list_data)))
        return str_data

    @staticmethod
    def convert_bytes(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
