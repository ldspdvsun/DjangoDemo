"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.static import serve
from django.urls import path, re_path
from django.conf import settings
from app01.views import depart, user, pretty, admin_manager, account, task, order, chart, upload, city

urlpatterns = [
    # 启用media
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # ====================== 用户登录管理 ======================
    # 登录
    path('login/', account.login),
    # 注销
    path('logout/', account.logout),
    # 验证码生成
    path('image/code/', account.image_code),

    # ====================== 部门管理 ======================
    # 部门列表
    path("depart/list/", depart.depart_list),
    # 新增部门
    path("depart/add/", depart.depart_add),
    # 删除部门
    path("depart/delete/", depart.depart_delete),
    # 修改部门
    # http://127.0.0.1:8000/depart/2/update
    path("depart/<int:edit_id>/update/", depart.depart_update),
    # 批量上传
    path("depart/multi/", depart.depart_multi),

    # ====================== 用户管理 ======================
    # 用户列表
    path("user/list/", user.user_list),
    # 新增用户
    path("user/add/", user.user_add),
    path("user/add_modelform/", user.user_add_modelform),
    # 删除用户
    path("user/delete/", user.user_delete),
    # 修改用户
    # http://127.0.0.1:8000/depart/2/update
    path("user/<int:edit_id>/update/", user.user_update),

    # 用户数据统计列表
    path("user/chart_list/", user.chart_list),
    # 用户数据统计折线图
    path("user/chart_line/", user.chart_line),
    # 用户数据统计柱状图
    path("user/chart_bar/", user.chart_bar),
    # 用户数据统计饼状图
    path("user/chart_pie/", user.chart_pie),
    # 获取用户数据统计界面x,y属性图
    path("user/get_chart_attributes/", user.get_chart_attributes),

    # ====================== 靓号管理 ======================
    # 靓号列表
    path("pretty/list/", pretty.pretty_list),
    # 新增靓号
    path("pretty/add/", pretty.pretty_add),
    # 删除靓号
    path("pretty/delete/", pretty.pretty_delete),
    # 修改靓号
    path("pretty/<int:edit_id>/update/", pretty.pretty_update),

    # ====================== 管理员管理 ======================
    # 管理员列表
    path("admin1/list/", admin_manager.admin_list),
    # 新增管理员
    path("admin1/add/", admin_manager.admin_add),
    # 删除管理员
    path("admin1/delete/", admin_manager.admin_delete),
    # 修改管理员
    path("admin1/<int:edit_id>/update/", admin_manager.admin_update),
    # 重置密码
    path("admin1/<int:edit_id>/reset/", admin_manager.admin_reset),

    # ====================== 任务管理 ======================
    # test ajax
    path("task/list/", task.task_list),
    path("task/ajax/", task.task_ajax),
    path("task/add/", task.task_add),

    # ====================== 订单管理 ======================
    # 订单列表
    path("order/list/", order.order_list),
    # 新增订单
    path("order/add/", order.order_add),
    # 删除订单
    path("order/delete/", order.order_delete),
    # 获取订单信息
    path("order/detail/", order.order_detail),
    # 修改订单
    path("order/edit/", order.order_edit),

    # ====================== 数据统计 ======================
    # 数据列表
    path("chart/list/", chart.chart_list),
    # 折线图
    path("chart/line/", chart.chart_line),
    # 柱状图
    path("chart/bar/", chart.chart_bar),
    # 饼状图
    path("chart/pie/", chart.chart_pie),

    # ====================== 上传文件 ======================
    path("upload/list/", upload.upload_list),
    path("upload/form/", upload.upload_form),
    path("upload/modelform/", upload.upload_modelform),

    # ====================== 城市列表 ======================
    path("city/list/", city.city_list),
    path("city/add/", city.city_add),
    path("city/delete/", city.city_delete),
    path("city/<int:edit_id>/update/", city.city_update),

]
