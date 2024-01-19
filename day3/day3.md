# day3 Django开发

- 部门管理
- 用户管理
  - 用户列表
  - 新建用户
    - ModelForm，针对数据库中的某个表。
    - Form。

# 续写day2代码

- 分页的逻辑和处理逻辑规则
  - 从头到尾开发
  - 写项目用【pagination.py】公共组件
- 小Bug, 搜索+分页情况下。

```
分页的时候保留原来的搜索条件
http://127.0.0.1:8000/pretty/list/?q=888
http://127.0.0.1:8000/pretty/list/?page=1

http://127.0.0.1:8000/pretty/list/?q=888&page=1
```

分页

### 10.时间插件

user_add.html

### 11.ModelForm和BootStrap

- ModelForm可以帮助我们生成HTML标签

  ```python
  class UserModelForm(forms.ModelForm):
      name = forms.CharField(min_length=3, laber="用户名")
      class Meta:
          model = models.UserInfo
          fields = ["name", "password"]
  form = UserModelForm()
  ```

  ```
  {{form.name}} 普通的input框
  {{form.password}} 普通的input框
  ```
- 定义插件

  ```python
  class UserModelFom(forms.ModelForm):
      class Meta:
          fields = {"name", "password", }

          widgets = {
              "name": forms.TextInput(attrs={"class":"form-control"})
              "password": forms.PasswordInput(attrs={"class": "form-control"})
              "age": forms.TextInput(attrs={"class": "form-control"}})
          }
  ```

  ```python
  class UserModelForm(forms.ModelForm):
      name = forms.CharField(min_length=3, laber="用户名", widget=forms.TextInput(attr={xxx}))
      class Meta:
          model = models.UserInfo
          fields = ["name", "password"]
  form = UserModelForm()
  ```
- 重新定义init方法，批量设置

  ```python
  class UserModelForm(forms.ModelForm):
      class Meta:
          model = models.UserInfo
          fields = ["name", "password"]
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          # 循环modelform中的所有字段，给每个字段的插件设置
          for name, field in self.fields.items():
              # 字段中有属性，保留原来的属性，没属性，才设置
              if field.widget.attrs:
                  field.widget.attrs["class"] = "form-control"
                  ......
              else:
                  field.widget.attrs = {
                      "class": "form-control",
                      "placeholder": filed.label,
                  }
  form = UserModelForm()
  ```
- 自定义类

  ```python
  class BootStrapForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          # 循环modelform中的所有字段，给每个字段的插件设置
          for name, field in self.fields.items():
              # 字段中有属性，保留原来的属性，没属性，才设置
              if field.widget.attrs:
                  field.widget.attrs["class"] = "form-control"
                  ......
              else:
                  field.widget.attrs = {
                      "class": "form-control",
                      "placeholder": filed.label,
                  }
  ```

  ```python
  class UserEditModelForm(BootStrapModelForm):
      class Meta:
           model = models.UserInfo
           fields = ["name", "password", "age"]
  ```
