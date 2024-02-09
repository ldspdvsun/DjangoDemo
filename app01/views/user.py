# coding=utf-8
"""
@File    : user.py
@Time    : 2024/2/5 9:50
@Author  : Sun
@Description : 用户管理功能 view
"""
from django.http import JsonResponse
from django.shortcuts import *
from app01.utils.pagination import Pagination
from app01.form.forms import *


def user_list(request):
    """用户列表"""
    # 界面搜索数据
    data_dict = {}
    search_name = request.GET.get('search_name', "")
    search_gender = request.GET.get('search_gender', "")
    if search_name:
        # name__contains 关键词匹配前端页面用户名name
        data_dict['name__contains'] = search_name
    if search_gender:
        # gender__contains 关键词匹配前端页面用户性别gender
        data_dict['gender__contains'] = search_gender

    search_result = models.UserInfo.objects.filter(del_flag=1, **data_dict).order_by("name")

    # 调用分页工具函数
    page_object = Pagination(request, search_result)

    context = {
        "search_result": search_result,
        "query_set": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    #
    # user_set = models.UserInfo.objects.filter(del_flag=1)
    #
    # for obj in user_set:
    #     # # 后端处理 格式化时间
    #     # obj.create_time = obj.create_time.strftime("%Y-%m-%d")
    #     #
    #     # # 后端处理 重新获取性别（1男0女）值
    #     # obj.gender = obj.get_gender_display()
    #
    #     # 获取部门名称
    #     # obj.depart.title
    #
    #     # 输出
    #     print(obj.id, obj.name, obj.account, obj.create_time, obj.gender, obj.depart.title)

    print('===================')
    print(page_object.page_queryset)
    print(page_object.page_queryset[0].gender)
    return render(request, "user/user_list.html", context)


def user_add_modelform(request):
    """新增用户（Modeform方式）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user/user_add_modelform.html', {"form": form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存数据
        # print(form.cleaned_data)
        form.save()
        return redirect("/user/list")

    return render(request, 'user/user_add_modelform.html', {"form": form})


def user_add(request):
    """新增用户（原始方式）"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.filter(del_flag=1).all()
        }

        return render(request, "user/user_add.html", context)

    # 获取前端页面数据
    user = request.POST.get('user')
    age = request.POST.get('age')
    gender = request.POST.get('gender')
    password = request.POST.get('password')
    account = request.POST.get('account')
    create_time = request.POST.get('create_time')
    depart_id = request.POST.get('depart')

    # 更新数据到数据库
    models.UserInfo.objects.create(name=user, age=age, gender=gender, password=password, account=account,
                                   create_time=create_time, depart_id=depart_id)

    # 重定向到列表页面
    return redirect("/user/list/")


def user_delete(request):
    """删除用户"""
    del_id = request.GET.get('del_id')

    # 逻辑删除
    models.UserInfo.objects.filter(id=del_id).update(del_flag=0)

    # 重定向到列表页面
    return redirect("/user/list/")


def user_update(request, edit_id):
    """更新用户"""
    # 根据ID获取要更新的对象
    edit_obj = models.UserInfo.objects.filter(id=edit_id).first()

    # 点击编辑后界面展示数据
    if request.method == "GET":
        # 通过instance获取要编辑对象的值
        form = UserModelForm(instance=edit_obj)
        return render(request, 'user/user_update.html', {"form": form})

    # 界面数据更新后更新数据库对象
    form = UserModelForm(data=request.POST, instance=edit_obj)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user/user_update.html', {'form': form})


def chart_list(request):
    """用户数据统计页面"""
    # 获取数据库表设计字段及名称，设置为字典
    model_attributes_verbose = {field.name: field.verbose_name for field in models.UserInfo._meta.get_fields() if
                                field.name != 'orders'}

    print(f'model_attributes_verbose:{model_attributes_verbose}')
    return render(request, "chart/user_chart_list.html",
                  {"model_attributes_verbose": model_attributes_verbose})


def get_chart_attributes(request):
    """用户数据统计页面 x,y轴 属性获取"""
    model_id_verbose = {field.name: field.verbose_name for field in models.UserInfo._meta.get_fields() if
                        field.name != 'orders'}
    if request.method == 'POST':
        x_key = request.POST.get('xValue')
        y_key = request.POST.get('yValue')
        x_value = model_id_verbose.get(x_key, "Unknown")
        y_value = model_id_verbose.get(y_key, "Unknown")
        print(x_key)
        print(y_key)
        print(x_value)
        print(y_value)

        # 在这里执行您希望的操作，例如将选中的 x 和 y 值传递给另一个视图函数进行处理
        result = {
            'X_KEY': x_key,
            'Y_KEY': y_key,
            'X_VALUE': x_value,
            'Y_VALUE': y_value,
        }
        return JsonResponse({'status': True, 'data': result})
    else:
        return JsonResponse({'status': False, 'error': 'Invalid request'})


def chart_line(request):
    """折线图数据"""
    # 数据库获取下列数据
    x_key = request.GET.get('xValue')
    y_key = request.GET.get('yValue')

    # 获取Y轴坐标的名称
    model_id_verbose = {field.name: field.verbose_name for field in models.UserInfo._meta.get_fields() if
                        field.name == y_key}
    y_value_legend = model_id_verbose.get(y_key, "Unknown")

    x_axis_list = list(models.UserInfo.objects.filter(del_flag=1).values_list(x_key, flat=True))
    series_data = list(models.UserInfo.objects.filter(del_flag=1).values_list(y_key, flat=True))

    series_list = [

        {
            "name": y_value_legend,
            "type": 'line',
            "stack": 'Total',
            "data": series_data
        },
    ]

    result = {
        "status": True,
        "data": {
            'x_axis_list': x_axis_list,
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


def chart_bar(request):
    """柱状图数据"""
    # 获取传递的 x 和 y 值
    x_key = request.GET.get('xValue')
    y_key = request.GET.get('yValue')
    print(x_key)
    print(y_key)

    # 获取Y轴坐标的名称
    model_id_verbose = {field.name: field.verbose_name for field in models.UserInfo._meta.get_fields() if
                        field.name == y_key}
    y_value_legend = model_id_verbose.get(y_key, "Unknown")

    # 使用传递的 x 值替换 x_axis_list 中的属性名
    x_axis_list = list(models.UserInfo.objects.filter(del_flag=1).values_list(x_key, flat=True))

    # 使用传递的 y 值替换 series_data 中的属性名
    series_data = list(models.UserInfo.objects.filter(del_flag=1).values_list(y_key, flat=True))

    series_list = [
        {
            "name": y_value_legend,
            "type": 'bar',
            "data": series_data,
        },
    ]

    result = {
        "status": True,
        "data": {
            'x_axis_list': x_axis_list,
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """饼状图数据"""
    # 数据库获取下列数据
    x_key = request.GET.get('xValue')
    y_key = request.GET.get('yValue')

    # 获取Y轴坐标的名称
    model_id_verbose = {field.name: field.verbose_name for field in models.UserInfo._meta.get_fields() if
                        field.name == y_key}
    y_value_legend = model_id_verbose.get(y_key, "Unknown")
    print(f'PIE y_value_legend:{y_value_legend}')

    x_axis_list = list(models.UserInfo.objects.filter(del_flag=1).values_list(x_key, flat=True))
    series_data = list(models.UserInfo.objects.filter(del_flag=1).values_list(y_key, flat=True))

    # 构建 series_data 列表
    series_data_list = [{"value": series_data[i], "name": x_axis_list[i]} for i in range(len(x_axis_list))]
    result = {
        "status": True,
        "name": y_value_legend,
        "data": {
            "series_data": series_data_list
        }
    }

    return JsonResponse(result)
