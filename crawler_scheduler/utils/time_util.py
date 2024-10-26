# -*- coding: utf-8 -*-


class TimeUtil(object):
    @classmethod
    def format_duration(cls, seconds):
        """
        将秒数格式化为时间字符串。
        
        Args:
            seconds (int): 秒数。
        
        Returns:
            str: 格式化后的时间字符串，格式为 '时:分:秒'。
        
        """
        """
        :param seconds: int
        :return: str
        """
        hour, second = divmod(seconds, 60 * 60)
        minute, second = divmod(second, 60)

        if hour > 0:
            delta = "{}h: {}m: {}s".format(hour, minute, second)
        elif minute > 0:
            delta = "{}m: {}s".format(minute, second)
        else:
            delta = "{}s".format(second)

        return delta
