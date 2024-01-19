from django.shortcuts import render, redirect
from app01 import models

def depart_list(request):
    """ 部门列表 """
    # 去数据库中获取所有的部门列表
    # [对象, ]
    queryset = models.Department.objects.all() 

    return render(request, 'depart_list.html', {'queryset': queryset})

def depart_add(request):
    """ 部门添加 """
    if request.method == "GET":
        return render(request, 'depart_add.html')
    # 获取用户提交过来的数据(title数据输入空怎么办)
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title=title)
    # 重定向回部门
    return redirect('/depart/list/')

def depart_delete(request):
    """ 删除部门 """
    # 获取id
    nid = request.GET.get('nid')
    # 删除
    models.Department.objects.filter(id=nid).delete()
    # 重定向回list
    return redirect('/depart/list/')

def depart_edit(request, nid):
    """ 修改部门 """
    # 根据nid，获取它的数据
    if request.method == "GET":
        # 根据nid，获取它的数据
        # row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id, row_object.title)
        # return render(request, 'depart_edit.html', {"row_object":row_object})
        # 上面代码可以简写为下面的代码
        return render(request, 'depart_edit.html', {"row_object":models.Department.objects.filter(id=nid).first()})
    # 根据id找到数据库的数据进行更新
    # update参数支持多个 update(xxx=xx, xxx2=xx2)
    models.Department.objects.filter(id=nid).update(title=request.POST.get('title'))
    return redirect('/depart/list/')