import json
from django import forms
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.forms.utils import ErrorDict
from app01 import models
from app01.utils.bootstrap import BootStrapModelForm

class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"
        widgets = {
            # "detail": forms.Textarea, # models里定义是TextField, 默认该组件
            "detail": forms.TextInput
        }
        
def task_list(request):
    """ 任务列表 """
    form = TaskModelForm()

    return render(request, "task_list.html", {"form": form})

@csrf_exempt # 免除scrf_token验证，ajax post
def  task_ajax(request):
    """ 测试ajax请求 """
    print("GET: ", request.GET) # <QueryDict: {'n1': ['123'], 'n2': ['456']}>
    print("POST: ", request.POST)
    data_dict = {"status": True, "data": [11,22,33,44]}
    json_string = json.dumps(data_dict)
    return HttpResponse(json_string)
    # return JsonResponse(data_dict)

@csrf_exempt
def task_add(request):
    """ 提交任务 """
    print(request.POST)

    # 1.用户发送过来的数据进行校验(ModelForm进行校验)
    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            # 2.保存数据到数据库
            task = form.save()
            # 3.返回成功信息
            data_dict = {"status": True, "data": task}
            json_string = json.dumps(data_dict)
            return HttpResponse(json_string)
        print(form.errors)
        data_dict = {"status": False, "error": form.errors}
        json_string = json.dumps(data_dict, ensure_ascii=False)
        return HttpResponse(json_string)
