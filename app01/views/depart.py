# coding=utf-8
"""
@File    : depart.py
@Time    : 2024/2/5 9:50
@Author  : Sun
@Description : 部门管理功能 view
"""
from django.shortcuts import *
from app01.form.forms import *
from openpyxl import *
import openpyxl
def depart_list(request):
    """查询部门列表"""
    depart_set = models.Department.objects.filter(del_flag=1).all()
    for obj in depart_set:
        print(obj.id, obj.title, obj.del_flag)
    # return HttpResponse("depart_list")
    return render(request, "depart/depart_list.html", {'depart_set': depart_set})


def depart_add(request):
    """新增部门"""
    if request.method == "GET":
        return render(request, "depart/depart_add.html")

    # 获取用户从前端页面提交的数据
    title = request.POST.get("title")
    models.Department.objects.create(title=title)

    # 重定向到列表页面
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    # http://127.0.0.1:8000/depart/delete/?del_id=1
    # 获取ID
    del_id = request.GET.get('del_id')

    # 逻辑删除
    models.Department.objects.filter(id=del_id).update(del_flag=0)

    # 重定向到列表页面
    return redirect("/depart/list/")


def depart_update(request, edit_id):
    """修改部门"""
    if request.method == 'GET':
        # 根据ID获取数据
        edit_obj = models.Department.objects.filter(id=edit_id).first()

        # 传递数据库中的值到前端页面
        return render(request, 'depart/depart_update.html', {"edit_obj": edit_obj})

    # 获取用户提交的内容
    new_title = request.POST.get("title")
    # 更新数据
    models.Department.objects.filter(id=edit_id).update(title=new_title)

    # 重定向到列表页面
    return redirect("/depart/list/")


def depart_multi(request):
    """基于Excel批量上传（Excel）"""
    # 1. 获取上传文件对象
    file_obj = request.FILES.get('xlsx')
    print(type(file_obj))

    # 2. 使用openpyxl 打开 excel,并读取
    wb = load_workbook(file_obj)
    sheet = wb.worksheets[0]

    # 3. 循环获取每一行数据
    for row in sheet.iter_rows(min_row=2):
        text = row[0].value
        exists = models.Department.objects.filter(title=text).exists()
        if not exists:
            models.Department.objects.create(title=text)

    return redirect("/depart/list/")
