# coding=utf-8
"""
@File    : account.py
@Time    : 2024/2/5 15:17
@Author  : Sun
@Description : 
"""
from django.shortcuts import *
from app01.form.forms import *
from app01.utils.pillow_code import check_code
from io import BytesIO


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 图片验证码校验
        user_input_image_code = form.cleaned_data.pop('code')
        real_image_code = request.session.get('image_code', "")
        if user_input_image_code != real_image_code:
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {'form': form})

        # 去数据库校验用户名和密码是否正确，获取用户对象、None
        # admin_object = models.Admin.objects.filter(username=xxx, password=xxx).first()
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            # form.add_error("username", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})

        # 用户名密码正确
        # 网站生成随机字符串，写到用户浏览器的cookie中
        request.session["info"] = {'id': admin_object.id, 'name': admin_object.username}

        # session 可以保存 24小时
        request.session.set_expiry(60 * 60 * 24)

        return redirect('/admin1/list/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """ 图片验证码生成 """
    # 调用Pillow函数，生成图片
    img, code_str = check_code()

    # 写入到自己的session中，（便于后续获取校验）
    request.session['image_code'] = code_str
    # 给session设置60s超时
    request.session.set_expiry(60)

    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())
