from django.db import models


# Create your models here.
class Admin(models.Model):
    username = models.CharField(verbose_name='管理员姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    del_flag = models.SmallIntegerField(verbose_name='删除标志', default=1)

    def __str__(self):
        return self.username


class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name='标题', max_length=32)
    del_flag = models.SmallIntegerField(verbose_name='删除标志', default=1)

    # 设置默认返回值
    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")
    # create_time = models.DateTimeField(verbose_name="入职时间")

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门ID")
    # 1.有约束
    #   - to，与那张表关联
    #   - to_field，表中的那一列关联
    # 2.django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 3.部门表被删除
    # ### 3.1 级联删除
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)
    # ### 3.2 置空
    # depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

    # 在django中做的约束
    gender_choices = (
        (1, "男"),
        (0, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    del_flag = models.SmallIntegerField(verbose_name='删除标志', default=1)

    def __str__(self):
        return self.name


class PrettyNum(models.Model):
    """靓号表"""
    # 手机号改为CharField不是IntegerField便于搜索匹配
    mobile = models.CharField(verbose_name='手机号', max_length=11)
    price = models.IntegerField(verbose_name='价格')
    level_choices = {
        (1, "黑铁级"),
        (2, "青铜级"),
        (3, "白银级"),
        (4, "黄金级"),
        (5, "钻石级"),
    }
    level = models.SmallIntegerField(verbose_name='级别', choices=level_choices, default=1)
    status_choices = {
        (0, "未占用"),
        (1, "已占用"),
    }
    status = models.IntegerField(verbose_name='状态', choices=status_choices, default=0)
    del_flag = models.IntegerField(verbose_name='删除标志', default=1)


class Task(models.Model):
    """任务"""
    title = models.CharField(verbose_name='标题', max_length=64)
    detail = models.TextField(verbose_name='详细信息')
    level_choices = {
        (1, "紧急"),
        (2, "重要"),
        (3, "一般"),
    }
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=3)
    del_flag = models.SmallIntegerField(verbose_name="删除标志", default=1)
    user = models.ForeignKey(verbose_name="负责人", to="Admin", on_delete=models.CASCADE)


class Orders(models.Model):
    """订单"""
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    status_choices = {
        (0, "未支付"),
        (1, "已支付"),
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=0)
    del_flag = models.SmallIntegerField(verbose_name="删除标志", default=1)
    user = models.ForeignKey(to=UserInfo, on_delete=models.CASCADE, verbose_name="用户")


class Boss(models.Model):
    """Boss"""
    name = models.CharField(verbose_name='姓名', max_length=32)
    age = models.IntegerField(verbose_name='年龄')
    img = models.CharField(verbose_name="Django文件路径", max_length=256, null=True, blank=True)
    img_real_path = models.CharField(verbose_name="实际文件路径", max_length=256, null=True, blank=True)

class City(models.Model):
    """ 城市 """
    name = models.CharField(verbose_name="名称", max_length=32)
    count = models.IntegerField(verbose_name="人口")

    # 本质上数据库也是CharField，自动保存数据。
    img = models.FileField(verbose_name="Logo", max_length=128, upload_to='city/')