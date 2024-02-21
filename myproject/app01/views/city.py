from django.shortcuts import render, redirect
from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm


def city_list(request):
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})

class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ['img']
    class Meta:
        model = models.City
        fields = "__all__"


def city_add(request):
    """ 上传文件和数据(ModelForm) """

    title = "添加城市"
    if request.method == 'GET':
        form = UpModelForm()
        return render(request, 'upload_form.html', {"form":form, 'title':title})

    form = UpModelForm(request.POST, request.FILES)
    if form.is_valid():
        # 自动上传保存到路径，路径写入数据库
        form.save() # 保存数据库

        return redirect('/city/list/') # 跳转到列表页面

    return render(request, 'upload_form.html', {"form":form, 'title':title})