from django.shortcuts import redirect, render, HttpResponse
from app01.models import Department, UserInfo

# render --> return html, 寻找模板，并返回
# 默认情况
# 重要，函数
# Create your views here.

def index(request):
    return HttpResponse("欢迎使用")

def user_list(request):
    # 如果setting文件模板设定了根目录，就会优先从根目录的templates目录下寻找
    # 1.去app目录下的templates目录找user_list.html(根据app里的注册顺序，逐一去他们的templates寻找)
    return render(request, "user_list.html")

def user_add(request):
    return render(request, "user_add.html")

def tpl(request):
    name = "Hermione"
    roles = ["管理员", "CEO", "保安"]
    user_info = {"name": "Hermione", "age": 18, "gender": "女", "role": "CEO"}
    data_list = [
        {"name": "Hermione", "age": 18, "gender": "女", "role": "CEO"},
        {"name": "Harry", "age": 18, "gender": "男", "role": "CTO"},
        {"name": "Ron", "age": 18, "gender": "男", "role": "CFO"},

    ]
    return render(request, "tpl.html", {"n1": name, "n2": roles, "n3":user_info, "n4":data_list})

def news(req):
    # 1.定义一些新闻（字典或者列表） 或者 去数据库  网络请求去联通新闻
    # 像地址：https://www.chinaunicom.com.cn/43/menu01/1/column05 发送请求
    import requests
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    res = requests.get("https://www.chinaunicom.com.cn/43/menu01/1/column05", headers= headers)
    # print(res.text)
    p = '<td width="1000" data-v-00a8aa21>(.*?)</td> <td align="right" width="200" class="time" data-v-00a8aa21>(2024-\d+-\d+)</td>'
    import re
    f = re.findall(p, res.text)# .reverse()
    return render(req, "news.html", {"news_list": f})

def something(request):
    # request是一个对象，封装了用户通过浏览器访问的所有数据
    # 1.获取请求方式 GET/POST
    print(request.method)
    # 2.在URL上传递值
    print(request.GET)
    # 3.通过请求体提交数据
    print(request.POST)

    # 4.【响应】HttpResponse 内容字符串内容返回给请求者
    #   【响应】render 读取html的内容，渲染(替换) --> 字符串，返回给用户浏览器

    # 5.【响应】让浏览器重定向
    # return redirect("www.baidu.com")
    return redirect("https://www.baidu.com")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # 如果是POST请求，获取用户提交的数据
        print(request.POST)
        username = request.POST.get("user")
        password = request.POST.get("pwd")
        if username == "admin" and password == "123456":
            return HttpResponse("登陆成功")
        else:
            # return HttpResponse("登录失败")
            return render(request, "login.html", {"msg": "用户名或密码错误"})
        
def orm(request):
    # 测试ORM操作表中的数据
    # ### 1.新建 ###
    # Department.objects.create(title="销售部")
    # Department.objects.create(title="IT部")
    # Department.objects.create(title="运营部")

    # UserInfo.objects.create(name="xll", password="123", age=18)
    # UserInfo.objects.create(name="xll2", password="123", age=18)

    # ### 2.删除 ###
    # filter 加筛选条件
    # UserInfo.objects.filter(name="xll2").delete()
    # UserInfo.objects.all().delete()

    # ### 3.获取数据 ###
    # data_list = [行，行，行], QuerySet数据
    data_list = UserInfo.objects.all()
    # 3.1 获取符合条件的所有数据
    # print(data_list)
    # for obj in data_list:
    #     print(obj.id, obj.name, obj.password)
    # data_list = UserInfo.objects.filter(name="xll")
    # print(data_list)
    ## 3.2获取第一条数据[对象]
    data = UserInfo.objects.filter(name="xll").first()
    print(data.id, data.name, data.password, data.age)

    ## #### 4.更新数据 ####
    UserInfo.objects.all().update(password="999")
    UserInfo.objects.filter(name="xll").update(password="123456")
    


    return HttpResponse("成功")

def info_list(request):
    # 1.获取数据库中所有的用户信息
    # [对象, ]
    data_list = UserInfo.objects.all()
    print(data_list)
    return render(request, "info_list.html", {"data_list": data_list} )

def info_add(request):
    if request.method == "GET":
        return render(request, 'info_add.html')
    # 获取用户提交的数据
    user = request.POST.get("user")
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')

    # 添加到数据库
    UserInfo.objects.create(name=user, password=pwd, age=age)
    # return HttpResponse("添加成功")
    # 自动跳转
    return redirect("/info/list/")

def info_delete(request):
    nid = request.GET.get("nid")
    UserInfo.objects.filter(id=nid).delete()
    # return HttpResponse("删除成功")
    return redirect("/info/list/")