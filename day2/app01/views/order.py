import random
from datetime import datetime
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.utils.bootstrap import BootStrapModelForm
from app01 import models
from app01.utils.pagination import Pagination

class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        # fields = "__all__"
        exclude = ["oid", "admin"]

def order_list(request):
    queryset = models.Order.objects.all().order_by("-id")
    page_object = Pagination(request, queryset)

    form = OrderModelForm()
    context = {
        "form": form,
        'queryset': page_object.queryset, # 分完页的数据
        "page_string":page_object.html(), # 页面
    }
    return render(request, "order_list.html", context)

@csrf_exempt
def order_add(request):
    """ 新建订单 (Ajax请求) """
    form = OrderModelForm(data=request.POST)
    if form.is_valid():
        # 额外增加一些用户输入的值
        # 订单号
        form.instance.oid = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        # 管理员 -- 当前登录的
        form.instance.admin_id = request.session["info"]["id"]
        form.save()
        return JsonResponse({"status": True}) # 内部字典序列化成json后提交
    return JsonResponse({"status": False, "error": form.errors}) # 序列化错误信息
    
def order_delete(request):
    """ 订单删除 """
    uid = request.GET.get("uid")
    # 也可以检验存不存在。
    if not models.Order.objects.filter(id=uid).exists():
        return JsonResponse({"status": False, "error": "删除失败，数据不存在"})
    models.Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True})

def order_detail(request):
    """ 订单编辑显示框 """
    ''' 方式1
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "error": "编辑失败，数据不存在"})
    
    # 从数据库获取一个对象，row_object
    row_dict = {
        "title": row_object.title,
        "price": row_object.price,
        "status": row_object.status
    }
    return JsonResponse({"status": True, "data": row_dict})
    '''
    
    # 方式2
    uid = request.GET.get("uid")
    row_dict = models.Order.objects.filter(id=uid).values("title", "price", "status").first()
    return JsonResponse({"status": True, "data": row_dict} if row_dict else {"status": False, "error": "数据不存在"})

@csrf_exempt
def order_edit(request):
    """ 订单编辑提交 """
    uid = request.GET.get("uid")
    row_object = models.Order.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status": False, "tips": "编辑失败，数据不存在，请刷新重试"})
    
    form = OrderModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({"status": False, "error": form.errors})
    
