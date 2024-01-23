from django.db import models

# Create your models here.

class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

class Department(models.Model):
    """部门表"""
    # varbose_name 是注解
    # id一般是自动设置，并且自增，也可以自己设置
    # id = models.BigAutoField(verbose_name='ID', primary_key=True)
    title = models.CharField(verbose_name='标题', max_length=32)

    def __str__(self):# 面向对象，打印对象返回值
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    # department = models.ForeignKey(Department, verbose_name="部门", on_delete=models.SET_NULL, null=True)

    # create_time = models.DateTimeField(verbose_name="入职时间")
    # date没有时分秒属性
    create_time = models.DateField(verbose_name="入职时间")
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门id")

    # 有约束
    #   - to, 与哪一张表关联
    #   - to_field, 表中的哪一列关联
    # django自动
    #   - 写的depart
    #   - 生成数据列 depart_id
    # 部门表被删除
    # 级联删除 - on_delete=models.CASCADE
    # 置空  - null=True, blank=True, on_delete=models.SET_NULL
    depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE, verbose_name="部门")

    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    
class PrettyNum(models.Model):
    """ 靓号管理表 """
    mobile = models.CharField(max_length=11, verbose_name="手机号")
    # 想要为空 null=True, blank=True
    price = models.IntegerField(verbose_name="价格", default=0)

    level_choices = ((1,"一级"),(2,"二级"),(3,"三级"),(4,"四级"))
    level = models.SmallIntegerField(choices=level_choices, default=4,verbose_name="级别")

    status_choices = ((1,"已占用"), (2,"未使用"))
    status = models.SmallIntegerField(choices=status_choices, default=2, verbose_name="状态")   

class Task(models.Model):
    """ 任务 """
    level_choices = (
        (1, "紧急"),
        (2, "重要"),
        (3, "临时")

    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="详情信息")

    user = models.ForeignKey(verbose_name="负责人", to="Admin", to_field="id", on_delete=models.CASCADE)
    

