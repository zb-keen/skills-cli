#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时间戳生成脚本
用于生成精确的时间戳，确保压缩文件名唯一
"""

import datetime


def get_timestamp():
    """
    生成时间戳
    :return: 格式化的时间戳字符串
    """
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hours = now.hour
    minutes = now.minute
    seconds = now.second
    
    formatted_month = f"{month:02d}"
    formatted_day = f"{day:02d}"
    formatted_hours = f"{hours:02d}"
    formatted_minutes = f"{minutes:02d}"
    formatted_seconds = f"{seconds:02d}"
    
    return f"{year}_{formatted_month}_{formatted_day}_{formatted_hours}_{formatted_minutes}_{formatted_seconds}"


if __name__ == "__main__":
    print("测试时间戳生成...")
    timestamp = get_timestamp()
    print(f"当前时间戳: {timestamp}")
