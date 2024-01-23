# day5 Django开发

知识点回顾

- 安装Django

  ```
  pip install django
  ```
- 创建Django项目

  ```
  >>> django-admin startproject mysite
  ```

    注意：Pycharm可以创建，但是需要settings.py中DIR templates删除

- 创建app & 注册

  ```
  >>> python mange.py startapp app01
  >>> python mange.py startapp app02
  >>> python mange.py startapp app03
  ```

  ```
  INSTALLED_APPS = [
      ...
      'app01.apps.App01Config',
  ]
  ```

    注意：一点要注册，否则app下的models.py写类是，无法在数据库中创建表

- 配置 静态文件路径 & 模板的路径 （放在app目录下）
- 配置数据库相关操作（如果使用文件数据库sqlite3，可以跳过数据库配置）

  - 第三方模块（django3版本）

    ```
    pip install mysqlclient
    ```
  - 自己先去mysql创建一个数据库。
  - 配置数据库链接settings.py

    ```
    DATABASES = {
        "default": {
            "ENGINE": 'django.db.backends.mysql',
            "NAME": "database",
            "USER": "root",
            "PASSWORD": "root123",
            "HOST": "127.0.0.1",
            "PORT": "3306",
        }
    }
    ```
  - 在app下的models.py中编写

    ```
    from django.db import models

    class Admin(models.Model):
        """ 管理员 """
        username = models.CharField(verbose_name='用户名', max_length=32)
        password = models.CharField(verbose_name="密码", max_length=64)

        def __str__(self): # models用到外键关联时，forms默认显示对象，__str__可以返回一个值显示
            return self.username
    ```
  - 执行两个命令：

  ```
  >>> python manage.py makemigrations
  >>> python manage.py migrate
  ```
- 在urls.py, 路由（URL 和 函数的对应关系）。
- 在views.py，视图函数，编写业务逻辑。
- templates目录，便携HTML模板（含有模板语法、继承、`{% static 'xx' %}`）
- ModelForm & Form 组件，在我们开发增删查改功能。

  - 生成HTML标签（生成默认值）
  - 请求数据进行校验
  - 保存到数据库（ModelForm）
  - 获取错误信息
- Cookie 和 Session, 用户登陆信息保存起来。
- 中间件，基于中间件实现用户认证，基于 `process_request`
- ORM操作

  ```
  models.User.objects.filter(id=xxx)
  models.User.objects.filter(id=xxx).order_by("-id")
  ```
- 分页组件。

## 1. Ajax请求

## 2.订单

订单表

| ID | 订单号     | 商品名称 | 价格 | 状态          | 用户id |
| -- | ---------- | -------- | ---- | ------------- | ------ |
| 1  | 2021111121 | 手机     | 1999 | 已支付/待支付 | 2      |
|    |            |          |      |               |        |

```python
class Order(models.Model):
    """ 工单 """
    oid = models.CharField(verbose_name="订单号", max_length=64)
    title = models.CharField(verbose_name="名称", max_length=32)
    price = models.IntegerField(verbose_name="价格")
    status_choices = {
        (1, "待支付"),
        (2, "已支付")
    }
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)

    admin = models.ForeignKey(verbose_name="管理员", to="Admin", to_field="id", on_delete=models.CASCADE)
  
```
