import re
from app01 import models
from django import forms
from app01.utils.bootstrap import BootStrapModelForm
from django.core.validators import RegexValidator

# ################################## ModelForm 实例 #############################
class UserModelForm(BootStrapModelForm):
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
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         # if name == "password":
    #         #     continue
    #         # print(name, field)
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

class PrettyModelForm(BootStrapModelForm):
    # 验证：方式1
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r"^\d{11}", "手机号格式错误"), ]
    # )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", 'price', 'level', 'status']
        # fields = "__all__"
        # exclude = ["level"] # xx字段除外
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         # if name == "password":
    #         #     continue
    #         # print(name, field)
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证：方式2 (钩子方法，可操作数据库)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exits = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exits:
            raise forms.ValidationError("手机号已存在")
        
        if len(txt_mobile) != 11:
            # 验证不通过
            raise forms.ValidationError("格式错误")
        # 校验通过，用户输入的值返回
        return txt_mobile
    
class PrettyEditModelForm(BootStrapModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    class Meta:
        model = models.PrettyNum
        # 不让它改手机号
        fields = ["mobile", "price", "level", "status"]
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {"class": "form-control", "placeholder": field.label}
    
    def clean_mobile(self): # 调用钩子函数，需要返回值，否则将其赋为空
        # 当前编辑哪一行的id
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise("手机号已经存在")
        m = re.match("^\d{11}$", txt_mobile)
        if not m:
            # 验证不通过
            raise forms.ValidationError("格式错误")
        # 校验通过，用户输入的值返回
        return txt_mobile