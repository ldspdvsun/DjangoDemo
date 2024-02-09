# coding=utf-8
"""
@File    : order.py
@Time    : 2024/2/6 21:36
@Author  : Sun
@Description : 订单 view
"""
import json
import random
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.models import *
from app01.form.forms import *
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination


def order_list(request):
    queryset = models.Orders.objects.all().filter(del_flag=1).order_by('-oid')
    page_object = Pagination(request, queryset)
    form = OrdersModelForm()

    context = {
        'form': form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }

    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """ 新建订单（Ajax请求）"""
    form = OrdersModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：额外增加一些不是用户输入的值（自己计算出来）
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))

        # 固定设置管理员ID，去哪里获取？
        form.instance.user_id = request.session["info"]["id"]

        # 保存到数据库中
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """ 删除订单 """
    uid = request.GET.get('uid')
    exists = models.Orders.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在。"})

    models.Orders.objects.filter(id=uid).update(del_flag=0)
    return JsonResponse({"status": True})


def order_detail(request):
    """ 根据ID获取订单详细 """
    # 方式1
    """
    uid = request.GET.get("uid")
    row_object = models.Orders.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": {
            "title": row_object.title,
            "price": row_object.price,
            "status": row_object.status,
        }
    }
    return JsonResponse(result)
    """

    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Orders.objects.filter(id=uid).values("title", 'price', 'status').first()
    if not row_dict:
        return JsonResponse({"status": False, 'error': "数据不存在。"})

    # 从数据库中获取到一个对象 row_object
    result = {
        "status": True,
        "data": row_dict
    }
    return JsonResponse(result)


@csrf_exempt
def order_edit(request):
    """ 编辑订单 """
    uid = request.GET.get("uid")
    row_object = models.Orders.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, 'tips': "数据不存在，请刷新重试。"})
    row_object.user_id = request.session["info"]["id"];
    form = OrdersModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})

    return JsonResponse({"status": False, 'error': form.errors})
