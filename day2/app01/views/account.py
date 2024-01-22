from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01 import models

# 这次尝试用form组件，不用ModelForm
## Form自定义数据，因为仅仅是校验
class LoginForm(BootStrapForm):
    username = forms.CharField(label="用户名",required=True)# required必填
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True)
    # username = forms.CharField(
    #     label="用户名",
    #     widget=forms.TextInput(attrs={"class": "form-control"}),
    # )
    # password = forms.CharField(
    #     label="密码",
    #     widget=forms.PasswordInput(attrs={"class": "form-control"}),
    # )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

## ModelForm是拿数据库的数据
# from app01 import models
# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model = models.Admin
#         fields = ["username", "password"]


def login(request):
    """ 登录 """
    if request.method == "GET":
        form = LoginForm()

        return render(request, "login.html", {"form": form})
    
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功获取到的用户名和密码, 然后去数据库校验
        # print(form.cleaned_data)
        # row_object = models.Admin.objects.filter(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        row_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if row_object:
            # 用户名和密码都正确
            # 网页生成随机字符串；写到用户浏览器cookie中；再写入session中；
            # request.session['info']会自动生成cookie，并存到session，并且info值也会加入到session数据里
            request.session['info'] = {"id":row_object.id, "name":row_object.username}
            return redirect("/admin/list/")
        
        form.add_error("username", "用户名或密码错误")
    return render(request, 'login.html', {"form": form})