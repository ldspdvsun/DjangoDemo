# coding=utf-8
"""
@File    : admin_manager.py
@Time    : 2024/2/5 10:01
@Author  : Sun
@Description : 自定义管理员功能 view
"""
from django.shortcuts import *
from app01.form.forms import *
from app01.utils.pagination import Pagination


def admin_list(request):
    """管理员列表"""
    # 检查用户是否登录，如果登录继续往下走，未登录则登录
    # 用户请求，获取生成的随机字符串，查看是否与数据库一致
    session_info = request.session.get("info")
    if not session_info:
        return redirect('/login/')




    # 界面搜索数据
    data_dict = {}
    search_data = request.GET.get('search', "")
    if search_data:
        # xxx__contains 关键词匹配前端页面用户名name
        data_dict['username__contains'] = search_data
    search_result = models.Admin.objects.filter(del_flag=1, **data_dict).order_by("username")

    # 调用分页工具函数
    page_object = Pagination(request, search_result)

    context = {
        "search_result": search_result,
        "query_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, "admin/admin_list.html", context)


def admin_add(request):
    """新增管理员"""
    title = "新增管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'public_add.html', {"form": form, "title": title})

    # 用户POST提交数据，数据校验
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin1/list")

    return render(request, 'public_add.html', {"form": form, "title": title})


def admin_delete(request):
    """删除用户"""
    del_id = request.GET.get('del_id')

    # 逻辑删除
    models.Admin.objects.filter(id=del_id).update(del_flag=0)

    # 重定向到列表页面
    return redirect("/admin1/list/")


def admin_update(request, edit_id):
    """更新管理员用户"""
    title = "编辑管理员"
    # 根据ID获取要更新的对象
    edit_obj = models.Admin.objects.filter(id=edit_id).first()

    # 点击编辑后界面展示数据
    if request.method == "GET":
        # 通过instance获取要编辑对象的值
        form = AdminEditModelForm(instance=edit_obj)
        # form = AdminModelForm(instance=edit_obj)
        return render(request, 'public_update.html', {"form": form, "title": title})

    # 界面数据更新后更新数据库对象
    form = AdminEditModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin1/list/')
    return render(request, 'public_update.html', {'form': form, "title": title})


def admin_reset(request, edit_id):
    """重置密码"""
    # 根据ID获取要更新的对象
    edit_obj = models.Admin.objects.filter(id=edit_id).first()
    if not edit_obj:
        return redirect("/admin1/list/")

    title = f"重置密码 - [{edit_obj.username}]"
    # 点击编辑后界面展示数据
    if request.method == "GET":
        # 通过instance获取要编辑对象的值
        form = AdminResetModelForm(instance=edit_obj)
        return render(request, 'public_update.html', {"form": form, "title": title})

    # 界面数据更新后更新数据库对象
    form = AdminResetModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/admin1/list/')
    return render(request, 'public_update.html', {'form': form, "title": title})
