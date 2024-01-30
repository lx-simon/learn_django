from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms

from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5
from app01 import models
from app01.utils.code import check_code

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
    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "请输入图片验证码"
            }
        ),
    )
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
        # 验证码的校验
        user_input_code = form.cleaned_data.pop("code")
        code = request.session.get("image_code", "")
        if code.upper() != user_input_code.upper():
            form.add_error("code", "验证码错误")
            return render(request, "login.html", {"form": form})

        # row_object = models.Admin.objects.filter(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
        row_object = models.Admin.objects.filter(**form.cleaned_data).first()
        if row_object:
            # 用户名和密码都正确
            # 网页生成随机字符串；写到用户浏览器cookie中；再写入session中；
            # request.session['info']会自动生成cookie，并存到session，并且info值也会加入到session数据里
            request.session['info'] = {"id":row_object.id, "name":row_object.username}
            # session保存7天，因为之前验证码设置了生存时间是60s，所以这边需要重置
            request.session.set_expiry(60 * 60 * 24 * 7)
            return redirect("/admin/list/")
        
        form.add_error("username", "用户名或密码错误")
    return render(request, 'login.html', {"form": form})

def logout(request):
    """ 注销 """
    request.session.clear()
    return redirect("/login/")

from io import BytesIO
def image_code(request,):
    """ 生成验证码图片 """
    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # print(code_string)
    # session每次登录都会生成，登录成功后会写入到服务端的数据库，过期时间内用户访问都可以用cookie
    # 写入到用户的session中，以便后续获取验证码进行校验
    request.session['image_code'] = code_string
    # 给session设置60s超时
    request.session.set_expiry(60)
    # 不保存图片后提取，保存到内存
    stream = BytesIO()
    img.save(stream, "png")
    
    return HttpResponse(stream.getvalue())