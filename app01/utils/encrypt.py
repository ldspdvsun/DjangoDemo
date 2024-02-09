# coding=utf-8
"""
@File    : encrypt.py
@Time    : 2024/2/5 10:55
@Author  : Sun
@Description : 密码加密
"""
import hashlib
from django.conf import settings

def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
