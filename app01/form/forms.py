# coding=utf-8
"""
@File    : forms.py
@Time    : 2024/2/5 9:47
@Author  : Sun
@Description : 
"""
from django import forms
from django.core.exceptions import ValidationError
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app01.utils.encrypt import md5
from django.core.validators import RegexValidator


class AdminModelForm(BootStrapModelForm):
    username = forms.CharField(
        min_length=3,
        label="管理员姓名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        # 密码隐藏输入
        widgets = {
            'password': forms.PasswordInput
        }

    # 密码加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    # 确认密码
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("密码不一致，请确认！！！")

        return confirm_password


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        # 密码隐藏输入
        widgets = {
            'password': forms.PasswordInput
        }

    # 密码加密
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 去数据库校保存的密码是否和新密码一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError("新密码不能与原先密码一致")
        return md5(pwd)

    # 确认密码
    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("密码不一致，请确认！！！")

        return confirm_password


class UserModelForm(BootStrapModelForm):
    name = forms.CharField(
        min_length=3,
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']


class PrettyModelForm(BootStrapModelForm):
    mobile = forms.CharField(
        min_length=11,
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        # 使用 exclude 排除 del_flag 属性
        exclude = ['del_flag']
        # __all__ 默认所有属性，排除 exclude 设置提前已经不展示的属性
        fields = "__all__"
        # 修改Models下已经定义好的属性
        widgets = {
            # "detail": forms.Textarea,
            "detail": forms.TextInput
        }


class OrdersModelForm(BootStrapModelForm):
    class Meta:
        model = models.Orders
        exclude = ['oid', 'del_flag', 'user']
        fields = "__all__"


class UploadForm(BootStrapForm):
    """上传文件 Form"""
    name = forms.CharField(label='姓名')
    age = forms.IntegerField(label='年龄')
    img = forms.FileField(label='头像')

    bootstrap_exclude_fields = ['img']


class CityModelForm(BootStrapModelForm):
    """上传文件 ModelForm"""
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = "__all__"
