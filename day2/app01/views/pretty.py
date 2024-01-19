import random
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import PrettyModelForm
from app01.utils.form import PrettyEditModelForm
# Create your views here.
def pretty_list(request):
    """ 靓号列表 """
    # 临时增加一些数据
    # for i in range(300):
    #     models.PrettyNum.objects.create(mobile=str(int("13800138000")+i), price=random.randint(1,100), level=1, status=2)

    # select * from table order by id asc
    # select * from table order by level desc

    data_dict = {}
    search_data = request.GET.get("q", "")
    if search_data:
        data_dict = {"mobile__contains":search_data}

    from app01.utils.pagination import Pagination

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")

    page_object = Pagination(request, queryset)

    page_queryset = page_object.queryset

    # # 1.根据用户想访问的页面，计算出值
    # page_size = 10
    # page = int(request.GET.get("page", 1))
    # start = (page-1) * page_size
    # end = page * page_size

    # queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[page_object.start:page_object.end]
    # print(queryset)
    # queryset = models.PrettyNum.objects.all().order_by("-level")

    # # 数据总条数
    # total_count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    # total_page_count, div = divmod(total_count, page_size)
    # if div: # 有余数，多一页
    #     total_page_count += 1

    page_string = page_object.html()

    context = {"search_data": search_data,
               'queryset': page_queryset, # 分完页的数据
               "page_string":page_string, # 页面
            }
    return render(request, 'pretty_list.html', context)

def pretty_add(request):
    """ 添加靓号 """
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    
    # 用户POST提交数据，数据校验
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/pretty/list/')
    # 校验失败 (页面上显示错误信息)
    # print(form.errors)
    return render(request, 'pretty_add.html', {'form': form})

def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, "pretty_edit.html", {"form":form})
    
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {"form":form})

def pretty_delete(request, nid):
    """ 靓号删除 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
