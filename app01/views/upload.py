# coding=utf-8
"""
@File    : upload.py
@Time    : 2024/2/7 22:37
@Author  : Sun
@Description : 文件上传
"""
import os.path

from django.conf import settings
from django.shortcuts import *
from django.http import JsonResponse
from app01.form.forms import *
from pathlib import Path


def upload_list(request):
    """文件上传"""
    if request.method == "GET":
        return render(request, "upload_list.html")

    print(request.POST)
    print(request.FILES)

    # 前端表单设计此 avatar值为文件上传
    file_object = request.FILES.get('avatar')
    print(f"file_object.name: {file_object.name}")

    # 上传文件
    with open(file_object.name, mode='wb') as f:
        for chunk in file_object.chunks():
            f.write(chunk)

    return HttpResponse("file")


def upload_form(request):
    """form格式文件上传"""
    title = "Form文件上传"
    if request.method == "GET":
        form = UploadForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = UploadForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        print(form.cleaned_data)
        # {'name': 'ALice', 'age': 22, 'img': <InMemoryUploadedFile: favicon.ico (image/x-icon)>}
        # 1. 读取图片内容，写入到文件夹，并获取文件的路径
        img_obj = form.cleaned_data.get('img')

        BASE_DIR = settings.MEDIA_ROOT
        # E:\PycharmProjects\Django\app01

        # 数据库存储路径，便于django查看静态文件，存储路径以static开始
        db_file_path = os.path.join("/media", img_obj.name)
        # 便于浏览器访问，将路径分隔符替换为“/”
        db_file_path = db_file_path.replace("\\", "/")

        # 实际存储路径
        file_path = os.path.join(BASE_DIR, img_obj.name)

        # E:\PycharmProjects\Django\app01\static\upload\favicon.ico
        with open(file_path, mode="wb") as f:
            for chunk in img_obj.chunks():
                f.write(chunk)

        # 2，将文件路径写入数据库
        models.Boss.objects.create(
            name=form.cleaned_data['name'],
            age=form.cleaned_data['age'],
            img=db_file_path,
            img_real_path=file_path,
        )

        print(BASE_DIR)
        print(file_path)

        return HttpResponse("...")
    return render(request, "upload_form.html", {"form": form, "title": title})


def upload_modelform(request):
    """ModelForm格式文件上传"""
    title = "ModelForm格式文件上传"
    if request.method == "GET":
        form = CityModelForm()
        return render(request, "upload_form.html", {"form": form, "title": title})

    form = CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 自动保存，上传文件到指定位置
        form.save()
        return HttpResponse("success")
    return render(request, "upload_form.html", {"form": form, "title": title})
