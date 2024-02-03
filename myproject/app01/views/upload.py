import os
from django.shortcuts import render, HttpResponse
from django import forms
from django.conf import settings
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from app01 import models

def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    # print(request.POST)
    # print(request.FILES)
    file_object = request.FILES.get('avatar')  # 获取上传的文件对象
    print(file_object.name) # 08f790529822720e0cf3722bfa821d46f21fbf097d82.jpeg
    
    for chunk in file_object.chunks():# 文件分块上传，也一点一点去读，chunk表示一块数据
        with open('a1.png', 'wb') as f:
            f.write(chunk)

    return HttpResponse(".....")


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

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"

def upload_model_form(request):
    """ 上传文件和数据(ModelForm) """

    title = "ModelForm上传"
    if request.method == 'GET':
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form":form, 'title':title})

    form = UpModelForm(request.POST, request.FILES)
    if form.is_valid():
        # 自动上传保存到路径，路径写入数据库
        form.save() # 保存数据库

        return HttpResponse("上传成功")

    return render(request, 'upload_form.html', {"form":form, 'title':title})