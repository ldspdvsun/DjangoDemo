# coding=utf-8
"""
@File    : task.py
@Time    : 2024/2/6 9:19
@Author  : Sun
@Description : 任务管理 view
"""
import json

import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from app01 import models
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.pagination import Pagination
from app01.form.forms import *

@csrf_exempt
def task_list(request):
    """ 任务列表 """
    # 去数据库获取所有的任务
    queryset = models.Task.objects.all().order_by('-id')
    page_object = Pagination(request, queryset)

    form = TaskModelForm()

    context = {
        "form": form,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 生成页码
    }
    return render(request, "task/task_list.html", context)

# Ajax POST 请求需要加入 @csrf_exempt
@csrf_exempt
def task_ajax(request):
    """任务列表"""
    print(request.GET)
    print('============================')
    print(request.POST)
    return HttpResponse(request.GET)
    # return HttpResponse('ajax success')
    # return render(request,"task_list.html")


@csrf_exempt
def task_add(request):
    # {'level': ['1'], 'title': ['sdfsdfsdfsd'], 'detail': ['111'], 'user': ['8']}
    # print(request.POST)

    # 1.用户发送过来的数据进行校验（ModelForm进行校验）
    form = TaskModelForm(data=request.POST)
    print(request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"status": False, 'error': form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))



def task_delete(request):
    """删除任务"""
    del_id = request.GET.get('del_id')

    # 逻辑删除
    models.Task.objects.filter(id=del_id).update(del_flag=0)

    # 重定向到列表页面
    return redirect("/task/list/")


def task_update(request, edit_id):
    """修改任务"""
    # 根据ID获取要更新的对象
    edit_obj = models.Task.objects.filter(id=edit_id).first()

    # 点击编辑后界面展示数据
    if request.method == "GET":
        # 通过instance获取要编辑对象的值
        form = TaskModelForm(instance=edit_obj)
        return render(request, 'task_update.html', {"form": form})

    # 界面数据更新后更新数据库对象
    form = TaskModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/task/list/')
    return render(request, 'task_update.html', {'form': form})
