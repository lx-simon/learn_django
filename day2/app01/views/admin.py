from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination

def admin_list(request):
    """ 管理员列表 """

    # 检查用户是否已经登陆，已登录，继续，未登录，跳转登陆
    # 用户发送请求，获取cookie随机字符串，那随机字符串查看有没有
    info = request.session.get("info")
    # print(info)
    if not info:
        return redirect('/login/')

    # 搜索
    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict = {"username__contains":search_data}

    # 根据搜索条件去数据库获取
    queryset = models.Admin.objects.filter(**data_dict)

    # 分页
    page_queryset = Pagination(request, queryset)
    context = {
        'queryset': page_queryset.queryset,
        'page_string': page_queryset.html()
    }
    return render(request, "admin_list.html", context)

from django import forms
from django.core.exceptions import ValidationError
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5

class AdminModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )
    class Meta:
        model = models.Admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),# 提交失败保留密码
        }

    # 执行按照fields顺序
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)
        

    def clean_confirm_password(self):
        # print(self.cleaned_data) {'username': 'alex', 'password': '123', 'confirm_password': '456'}
        confirm = md5(self.cleaned_data.get("confirm_password"))
        password = self.cleaned_data.get("password")
        if confirm != password:
            raise ValidationError("两次密码不一致")
        # 返回什么，此字段以后保存到数据库是什么。
        return confirm

class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ["username"]
        # widgets = 

def admin_add(request):
    """ 添加管理员 """
    title = "新增管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request, "change.html", {"title": title, "form": form})
    
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form":form, "title":title})

def admin_edit(request, nid):
    """ 编辑管理员 """

    # 对象
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg":"数据不存在"})

    title = "编辑管理员"
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)

        return render(request, 'change.html', {"form": form, "title":title})
    
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form":form, "title":title})

def admin_delete(request, nid):
    ''' 删除管理员 '''
    # 可以先获取后删
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

class AdminResetModelForm(BootStrapModelForm):
    confire_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True),
    )
    class Meta:
        model = models.Admin
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True),
        }

    # 执行按照fields顺序
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        # 去数据库校验一下，看数据库密码和输入是否一致
        print("看看self.instance.id：",self.instance.id)
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()

        if exists:
            raise ValidationError("密码不能和原密码一致")

        return md5_pwd

    def clean_confirm_password(self):
        # print(self.cleaned_data) {'username': 'alex', 'password': '123', 'confirm_password': '456'}
        confirm = md5(self.cleaned_data.get("confirm_password"))
        password = self.cleaned_data.get("password")
        if confirm != password:
            raise ValidationError("两次密码不一致")
        # 返回什么，此字段以后保存到数据库是什么。
        return confirm

def admin_reset(request, nid):
    """ 重置管理员密码 """
    # 对象 / None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return render(request, 'error.html', {"msg":"数据不存在"})

    title = "重置密码 - {}".format(row_object.username)

    if request.method == "GET":
        form = AdminResetModelForm()
        return render(request, "change.html", {"title":title, "form":form})
    
    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'error.html', {"msg":"数据不存在"})