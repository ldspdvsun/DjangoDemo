# coding=utf-8
"""
@File    : tools.py
@Time    : 2024/2/6 22:56
@Author  : Sun
@Description : 公用的工具类
"""
import random
from datetime import datetime

def generate_order_id():
    """
    生成订单ID
    :return: order_id 202402062301001000 - 202402062301009999
    """
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")+str(random.randint(1000,9999))
    return order_id