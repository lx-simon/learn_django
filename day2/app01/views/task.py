import json
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def task_list(request):
    """ 任务列表 """
    return render(request, "task_list.html")

@csrf_exempt # 免除scrf_token验证，ajax post
def  task_ajax(request):
    """ 测试ajax请求 """
    print("GET: ", request.GET) # <QueryDict: {'n1': ['123'], 'n2': ['456']}>
    print("POST: ", request.POST)
    data_dict = {"status": True, "data": [11,22,33,44]}
    json_string = json.dumps(data_dict)
    return HttpResponse(json_string)
    # return JsonResponse(data_dict)