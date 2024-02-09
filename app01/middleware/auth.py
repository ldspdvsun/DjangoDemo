# coding=utf-8
"""
@File    : auth.py
@Time    : 2024/2/5 21:22
@Author  : Sun
@Description : 用户登录中间件
"""
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class AutoMiddleware(MiddlewareMixin):
    """认证中间件"""

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        #   request.path_info 获取当前用户请求的URL /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1.读取当前访问的用户的session信息，如果能读到，说明已登陆过，就可以继续向后走。
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 2.没有登录过，重新回到登录页面
        return redirect('/login/')


# class Middleware1(MiddlewareMixin):
#     """中间件1"""
#
#     def process_request(self, request):
#         # 如果方法没有返回值或者为None,继续向后走
#         # 如果有返回值 HttpResponse,render,redirect
#         print("Middleware1 进来了")
#
#     def process_response(self, request, response):
#         print("Middleware1 走了")
#         return response
#
# class Middleware2(MiddlewareMixin):
#     """中间件2"""
#
#     def process_request(self, request):
#         print("Middleware2 进来了")
#
#     def process_response(self, request, response):
#         print("Middleware2 走了")
#         return response
