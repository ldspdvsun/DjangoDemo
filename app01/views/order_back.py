# coding=utf-8
"""
@File    : order.py
@Time    : 2024/2/6 21:36
@Author  : Sun
@Description : 订单 view
"""
from django.shortcuts import *
from django.http import JsonResponse
from app01.form.forms import OrdersModelForm
from django.views.decorators.csrf import csrf_exempt

from app01.utils.tools import generate_order_id
from django import forms
from django.shortcuts import *
from app01 import models
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator
from app01.form.forms import *
from app01.models import Orders


def order_list(request):
    """订单列表"""
    queryset = models.Orders.objects.filter(del_flag=1).order_by('-oid')
    page_object = Pagination(request, queryset)
    form = OrdersModelForm()
    title = "订单列表"
    context = {
        "form": form,
        "title": title,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, 'order_list.html', context)


@csrf_exempt
def order_add(request):
    """新增订单(Ajax)请求"""
    form = OrdersModelForm(data=request.POST)
    if form.is_valid():
        # 订单号：额外增加一些不是用户输入的值，而是自己增加的值 form.instance.oid
        form.instance.oid = generate_order_id()

        # 默认获取登录的用户的ID，作为添加数据的ID(此处因为测试原因绑定的外键为用户表的ID，但是session获取的却是管理员登录的ID，
        # 如果出错，可重新调整表结构绑定外键为管理员)
        form.instance.user_id = request.session['info']['id']

        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})


def order_delete(request):
    """删除订单"""
    del_id = request.GET.get('del_id')
    exists = models.Orders.objects.filter(id=del_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "删除失败，数据不存在！"})
    models.Orders.objects.filter(id=del_id).update(del_flag=0)
    return JsonResponse({"status": True})


def order_detatil(request):
    """获取订单信息"""
    """ 方式1
    edit_id = request.GET.get("edit_id")
    exists = models.Orders.objects.filter(id=edit_id).exists()
    if not exists:
        return JsonResponse({"status": False, 'error': "数据不存在！"})
    # 从数据库获取对象
    edit_obj = models.Orders.objects.filter(id=edit_id).first()
    result = {
        "title": edit_obj.title,
        "price": edit_obj.price,
        "status": edit_obj.status,
    }
    return JsonResponse({"status": True, "data": result})
    """
    # 方式2
    edit_id = request.GET.get("edit_id")
    # 从数据库获取字典
    edit_dict = models.Orders.objects.filter(id=edit_id).values('title', 'price', 'status').first()
    if not edit_dict:
        return JsonResponse({"status": False, 'error': "数据不存在！"})
    return JsonResponse({"status": True, "data": edit_dict})


from django.shortcuts import get_object_or_404


@csrf_exempt
def order_update(request):
    """更新订单"""
    edit_id = request.GET.get('edit_id')
    edit_obj = models.Orders.objects.filter(id=edit_id).first()
    if not edit_obj:
        return JsonResponse({"status": False, 'errors': "数据不存在"})

    form = OrdersModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, 'error': form.errors})

    # copy_post_data = request.POST.copy()
    # edit_id = request.GET.get('edit_id')
    #
    # form = OrdersModelForm(data=copy_post_data)
    #
    # title = request.POST.get("title")
    # price = request.POST.get("price")
    # status = request.POST.get("status")
    # user_id = request.session['info']['id']
    #
    # print(request.POST)
    # print(copy_post_data)
    #
    # if form.is_valid():
    #     models.Orders.objects.filter(id=edit_id).update(title=title, price=price, status=status, user_id=user_id)
    #     return JsonResponse({"status": True})
    # return JsonResponse({"status": False, 'error': form.errors})

    # print(request.POST)
    # 获取编辑订单的ID <QueryDict: {'title': ['5asd'], 'price': ['50.00'], 'status': ['0'], 'edit_id': ['13']}>
    # edit_id = request.POST.get('edit_id')
    # title = request.POST.get("title")
    # price = request.POST.get("price")
    # status = request.POST.get("status")
    # user_id = request.session['info']['id']
    # if not edit_id:
    #     return JsonResponse({"status": False, 'error': "数据不存在！"})
    # models.Orders.objects.filter(id=edit_id).update(title=title, price=price, status=status, user_id=user_id)
    # return JsonResponse({"status": True})
