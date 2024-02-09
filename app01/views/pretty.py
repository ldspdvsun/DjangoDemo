# coding=utf-8
"""
@File    : pretty.py
@Time    : 2024/2/5 9:50
@Author  : Sun
@Description : 靓号管理功能view
"""
from django import forms
from django.shortcuts import *
from app01 import models
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator
from app01.form.forms import *


def pretty_list(request):
    """靓号列表"""

    # 界面搜索数据
    data_dict = {}
    search_data = request.GET.get('search', "")
    if search_data:
        # mobile__contains 关键词匹配前端页面 手机号mobile
        data_dict['mobile__contains'] = search_data
    search_result = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    # 调用分页工具函数
    page_object = Pagination(request, search_result)

    context = {
        "search_result": search_result,
        "query_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, "pretty/pretty_list.html", context)


def pretty_add(request):
    """新增靓号"""
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty/pretty_add.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pretty/list")

    return render(request, 'pretty/pretty_add.html', {"form": form})


def pretty_delete(request):
    """删除靓号"""
    del_id = request.GET.get('del_id')

    # 逻辑删除
    models.PrettyNum.objects.filter(id=del_id).update(del_flag=0)

    # 重定向到列表页面
    return redirect("/pretty/list/")


def pretty_update(request, edit_id):
    """修改靓号"""
    # 根据ID获取要更新的对象
    edit_obj = models.PrettyNum.objects.filter(id=edit_id).first()

    # 点击编辑后界面展示数据
    if request.method == "GET":
        # 通过instance获取要编辑对象的值
        form = PrettyModelForm(instance=edit_obj)
        return render(request, 'pretty/pretty_update.html', {"form": form})

    # 界面数据更新后更新数据库对象
    form = PrettyModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty/pretty_update.html', {'form': form})
