# coding=utf-8
"""
@File    : chart.py
@Time    : 2024/2/7 19:48
@Author  : Sun
@Description : 数据统计图形列表
"""
from django.http import JsonResponse
from django.shortcuts import *


def chart_list(request):
    """数据统计页面"""
    return render(request, "chart/chart_list.html")


def chart_line(request):
    """折线图数据"""
    # 数据库获取下列数据

    legend = ['第1分公司', '第2分公司', '第3分公司', '第4分公司', '第5分公司']
    x_axis_list = ['1月', '2月', '3月', '4月', '5月', '6月', '7月']
    series_list = [

        {
            "name": '第1分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]
        },
        {
            "name": '第2分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [220, 182, 191, 234, 290, 330, 310]
        },
        {
            "name": '第3分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [150, 232, 201, 154, 190, 330, 410]
        },
        {
            "name": '第4分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [320, 332, 301, 334, 390, 330, 320]
        },
        {
            "name": '第5分公司',
            "type": 'line',
            "stack": 'Total',
            "data": [820, 932, 901, 934, 1290, 1330, 1320]
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'x_axis_list': x_axis_list,
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


def chart_bar(request):
    """柱状图数据"""
    # 数据库获取下列数据
    legend = ["Alice", "John"]
    x_axis_list = ['1月', '2月', '3月', '4月', '5月', '6月']
    series_list = [
        {
            "name": 'Alice',
            "type": 'bar',
            "data": [50, 120, 36, 10, 10, 20]
        },
        {
            "name": 'John',
            "type": 'bar',
            "data": [15, 30, 36, 120, 100, 20]
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'x_axis_list': x_axis_list,
            'series_list': series_list,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    """饼状图数据"""
    # 数据库获取下列数据

    result = {
        "status": True,
        "data": {
            "series_data": [
                {"value": 1048, "name": 'IT部门'},
                {"value": 735, "name": '人事部'},
                {"value": 580, "name": '行政部'},
                {"value": 484, "name": '后勤部'},
                {"value": 300, "name": '财务部'}

            ]
        }
    }

    return JsonResponse(result)
