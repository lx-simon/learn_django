import random
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination
from app01.utils.form import UserModelForm
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

    page_object = Pagination(request, queryset)
    context = {
        "queryset": page_object.queryset, # 分完页的数据
        "page_string":page_object.html(), # 页面
    }

    return render(request, 'user_list.html', context)

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

def user_model_form_add(request):
    """ 添加用户（ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_model_form_add.html', {"form":form})
    
    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # 如果数据合法，保存到数据库
        # {'name': '黄钜明', 'password': '12345', 'age': 24, 'account': Decimal('0'), 'create_time': datetime.datetime(2019, 2, 12, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'depart': <Department: IT运维>}
        # models.UserInfo.objects.create(**form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    # 校验失败 (页面上显示错误信息)
    # print(form.errors)
    return render(request, 'user_model_form_add.html', {"form":form})

def user_edit(request, nid):
    """ 编辑用户 """
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID去数据库获取要编辑那一行数据(对象)
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存用户输入的所有数据，如果需要用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})

def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

