from django.shortcuts import render, redirect
from app01 import models
# Create your views here.
def depart_list(request):
    """ 部门列表 """
    # 去数据库中获取所有的部门列表
    # [对象, ]
    queryset = models.Department.objects.all() 

    return render(request, 'depart_list.html', {'queryset': queryset})

def depart_add(request):
    """ 部门添加 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户提交过来的数据(title数据输入空怎么办)
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门
    return redirect('/depart/list/')

def depart_delete(request):
    """ 删除部门 """
    # 获取id
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 重定向回list
    return redirect('/depart/list/')

def depart_edit(request, nid):
    """ 修改部门 """
    # 根据nid，获取它的数据
    if request.method == "GET":
        # 根据nid，获取它的数据
        # row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id, row_object.title)
        # return render(request, 'depart_edit.html', {"row_object":row_object})
        # 上面代码可以简写为下面的代码
        return render(request, 'depart_edit.html', {"row_object":models.Department.objects.filter(id=nid).first()})
    # 根据id找到数据库的数据进行更新
    # update参数支持多个 update(xxx=xx, xxx2=xx2)
    models.Department.objects.filter(id=nid).update(title=request.POST.get('title'))
    return redirect('/depart/list/')

def user_list(request):
    """ 用户管理 """
    queryset = models.UserInfo.objects.all()
    # python内部和模板内部数据处理不太一样
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.get_gender_display(), obj.depart.title)
        # 1 刘东 100.68 2020-11-11 00:00:00+00:00 <class 'datetime.datetime'>
        # obj.gender #1/2
        # obj.get_gender_display() #男/女 # get_字段名称_display()
        # obj.depart # <Department: 部门>
        # obj.depart_id # 获取数据库中存储的那个字段值
        # models.Department.objects.filter(id=obj.depart_id).first().title
        # obj.depart.title # 根据id自动关联表中获取那一行数据的对象

    return render(request, 'user_list.html', {'queryset': queryset})

def user_add(request):
    """ 添加用户 """
    if request.method == "GET":
        # 获取所有的部门列表
        gender_list = models.UserInfo.gender_choices
        depart_list = models.Department.objects.all()
        return render(request, 'user_add.html', {'depart_list': depart_list, 'gender_list':gender_list})
    
    # 获取用户提交过来的数据
    name = request.POST.get("username")
    password = request.POST.get("passwd")
    age = request.POST.get("age")
    gender = request.POST.get("gender")
    create_time = request.POST.get("ctime")
    depart_id = request.POST.get("dp")

    # 保存到数据库
    models.UserInfo.objects.create(name=name,password=password,age=age,gender=gender,create_time=create_time,account=0.0,depart_id=depart_id)
    return redirect('/user/list/')

# ################################## ModelForm 实例 #############################
from django import forms
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=2, label="用户名")
    # password = forms.CharField(label="密码", validators="[A-Za-z0-9]{6,}")
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "account", "create_time", "gender", "depart"]
        # widgets = {
        #     # form加上标签
        #     "name": forms.TextInput({"class":"form-control"}),
        #     "password": forms.PasswordInput({"class":"form-control"}),
        #     "age": forms.TextInput({"class":"form-control"}),
        # }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            # print(name, field)
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form":form})
    
    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # 如果数据合法，保存到数据库
        # {'name': '黄钜明', 'password': '12345', 'age': 24, 'account': Decimal('0'), 'create_time': datetime.datetime(2019, 2, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'depart': <Department: IT运维>}
        # models.UserInfo.objects.create(**form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    # 校验失败 (页面上显示错误信息)
    # print(form.errors)
    return render(request, 'user_model_form_add.html', {"form":form})
