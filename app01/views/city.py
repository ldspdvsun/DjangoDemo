# coding=utf-8
"""
@File    : city.py
@Time    : 2024/2/8 10:06
@Author  : Sun
@Description : 
"""

from django.forms import *
from django.shortcuts import *
from app01 import models
from app01.form.forms import CityModelForm


def city_list(request):
    """城市列表"""
    query_set = models.City.objects.all()
    return render(request, "city_list.html", {"query_set": query_set})


def city_add(request):
    """新增城市"""
    title = "新增城市"
    if request.method == "GET":
        form = CityModelForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 自动保存，上传文件到指定位置
        form.save()
        return redirect("/city/list/")
    return render(request, "upload_form.html", {"form": form, "title": title})


def city_delete(request):
    """删除城市"""
    # 获取ID
    del_id = request.GET.get('del_id')

    # 物理删除
    models.City.objects.filter(id=del_id).delete()

    # 重定向到列表页面
    return redirect("/city/list/")


def city_update(request, edit_id):
    """修改城市"""
    # 根据ID获取要更新的对象
    edit_obj = models.City.objects.filter(id=edit_id).first()

    # 点击编辑后界面展示数据
    if request.method == "GET":
        # 通过instance获取要编辑对象的值
        form = CityModelForm(instance=edit_obj)
        return render(request, 'city_update.html', {"form": form})

    # edit_obj.img = request.FILES.get('img')
    # 界面数据更新后更新数据库对象
    form = CityModelForm(data=request.POST, files=request.FILES, instance=edit_obj)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/city/list/')
    return render(request, 'city_update.html', {'form': form})
