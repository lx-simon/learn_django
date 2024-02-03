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

```python
# 对象、当前行的所有数据
row_object = models.Order.objects.filter(id=uid).first()
row_object.id
row_object.title

# 字典 {"id": xxx, "title": xxxxx}
row_dict = models.Order.objects.filter(id=uid).values("id", "title").first()

# queryset = [obj, obj, ]
queryset = models.Order.objects.all()

# queryset = [dict, dict, ]
queryset = models.Order.objects.all().values("id", "title")

# queryset = [ (id, title), ]
queryset = models.Order.objects.all().values_list("id", "title")

```

## 3.图表

- highchar, 国外。
- echarts, 国内。

更多参考官方文档。

## 4.文件上传

基本操作

```
        <!-- enctype加上后才支持上传文件内容 -->
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            <input type="text" name="username">
            <input type="file" name="avatar">
            <input type="submit" value="提交">
        </form>
```

```python
print(request.POST)
print(request.FILES)
```

### 案例：批量上传

```
            <div class="panel-body">
                <form method="post" enctype="multipart/form-data" action="/depart/multi/">
                    {% csrf_token %}
                    <div class="form-group">
                        <input type="file" name="exc">
                    </div>
                    <input type="submit" value="上传" class="btn btn-info btn-sm">
                </form>
            </div>
```

```
def depart_multi(request):
    """ 通过文件批量上传 """
    # 获取文件
    file_obj = request.FILES.get("exc")
    print(type(file_obj))
    # 读取文件
    wb = load_workbook(file_obj)
    # 获取sheet
    sheet = wb.worksheets[0]
    # 循环获取每一行数据
    for row in sheet.iter_rows(2):
        text = row[0].value
        print(text)
        exists = models.Department.objects.filter(title=text)
        if not exists:
            models.Department.objects.create(title=text)

    return redirect('/depart/list/')
```

### 案例： 混合数据

提交页面时：用户输入数据+文件（数据不为空，报错）

- Form生成HTML标签：type+file
- 表单的验证
- form.cleaned_data 获取数据+文件名

  ```python
  class UpForm(BootStrapForm):
      bootstrap_exclude_fields = ['img']

      name = forms.CharField(label='姓名', max_length=32)
      age = forms.IntegerField(label='年龄')
      img = forms.FileField(label='头像')


  def upload_form(request):
      """ 文件Form上传 """
      title = "Form上传"
      if request.method == 'GET':
          form = UpForm()
          return render(request, 'upload_form.html', {"form":form, 'title':title})
    
      form = UpForm(request.POST, request.FILES)
      if form.is_valid():
          # print(form.cleaned_data)
          # 1. 保存图片内容，写入到文件夹并保存到文件的路径种
          image_object = form.cleaned_data.get('img')
          # file_path = "app01/image/"
          db_file_path = os.path.join('static', 'img', image_object.name)
          file_path = os.path.join('app01', 'static', 'img', image_object.name)
          with open(file_path, mode='wb') as f:
              for chunk in image_object.chunks():
                  f.write(chunk)
          # 2. 保存图片的路径名保存到数据库中
          models.Boss.objects.create(
              name=form.cleaned_data.get('name'),
              age=form.cleaned_data.get('age'),
              avatar=db_file_path,
          )
          return HttpResponse("上传成功")
    
      return render(request, 'upload_form.html', {"form":form, 'title':title})
  ```

```html
{% extends 'layout.html' %}

{% block content %}
<div class="container">
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title"> {{ title }} </h3>
        </div>
        <div class="panel-body">
            <form method="post" enctype="multipart/form-data" novalidate>
                {% csrf_token %}
                {% for field in form %}
                    <div class="form-group">
                    <!-- label 就是models 定义verbose_name -->
                    <label>{{ field.label }}</label>
                    {{ field }}
                    <!-- [错误1, 错误2, ...] -->
                    <span style="color:red;">{{ field.errors.0 }}</span>
                    <!-- <input type="text" class="form-control" placeholder="" -->
                    </div>
                {% endfor %}

                <button type="submit" class="btn btn-primary">保 存</button>
            </form>
        </div>
    </div>
</div>

{% endblock %}

```

- 写入图片文件非得写道static才能访问? django目前所有静态文件只能放在static目录

在django的开发过程中两个文件夹比较特殊：

- static，存放静态文件的路径，包括：CSS, JS, 项目图片
- media, 用户上传数据的目录。
  - 启动media配置
    - 在urls.py中进行配置

      ```python
      urlpatterns = [
          re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name="media"),
      ]
      ```
    - 在settings进行配置

      ```python
      # media文件访问配置
      MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
      MEDIR_URL = "/media/"
      ```
    - ```
      def upload_form(request):
          """ 文件Form上传 """
          title = "Form上传"
          if request.method == 'GET':
              form = UpForm()
              return render(request, 'upload_form.html', {"form":form, 'title':title})
        
          form = UpForm(request.POST, request.FILES)
          if form.is_valid():
              # print(form.cleaned_data)
              # 1. 保存图片内容，写入到文件夹并保存到文件的路径种
              image_object = form.cleaned_data.get('img')
              # 用os是方便不同操作系统?
            
              # 绝对路径
              # media_path = os.path.join(settings.MEDIA_ROOT, image_object.name)
              media_path = os.path.join('media', image_object.name)

              with open(media_path, mode='wb') as f:
                  for chunk in image_object.chunks():
                      f.write(chunk)
              # 2. 保存图片的路径名保存到数据库中
              models.Boss.objects.create(
                  name=form.cleaned_data.get('name'),
                  age=form.cleaned_data.get('age'),
                  avatar=media_path,
              )
              return HttpResponse("上传成功")
        
          return render(request, 'upload_form.html', {"form":form, 'title':title})
      ```

### 案例: 混合数据（ModelForm)

- 修改models.py文件

  ```python
  class City(models.Model):
      """ 城市 """
      name = models.CharField(verbose_name="城市名称", max_length=32)
      count = models.IntegerField(verbose_name="人口数量")
      # 本质上数据库也是CharField
      img = models.FileField(verbose_name="logo", max_length=256, upload_to="city/")

  ```

#### 定义ModelForm

```python
def upload_model_form(request):
    """ 上传文件和数据(ModelForm) """
    bootstrap_exclude_fields = ['img']

    title = "ModelForm上传"
    if request.method == 'GET':
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form":form, 'title':title})

```

## 小结

- 自己动手去写

  ```
  file_object = request.FILES.get("exc")
  ```
- Form组件(表单验证)

  ```
  request.POST
  xxxxxxxxxxxxxxxx
  ```
- ModelForm (表单验证+自己保存数据库+自动保存文件)

  ```
  - media
  - Model.py filefield
  ```
