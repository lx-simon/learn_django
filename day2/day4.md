# day4 Django开发

## 12.管理员操作

| id | username | password |
| -- | -------- | -------- |
|    |          |          |
|    |          |          |

```
mysql -u root -p;
show databases;
use day2;
# django创建表格式 app_+字段名小写
desc app01_admin;
insert into app01_admin(username, password) values("xll", "123");
select * from app01_admin;
```

## 13.用户登陆

什么是cookie和session？

- 浏览器网址的通过http请求，无状态的短链接
  ![1705824491253](image/day4/1705824491253.png)

  ![1705824967671](image/day4/1705824967671.png)

### 13.1 登陆

- cookie, 随机子串
- session, 用户信息

在其他需要登陆才能访问的页面都要加入

```python
info = request.session.get("info")
    # print(info)
    if not info:
        return redirect('/login/')
```

目标：在18个视图函数加入判断


### 13.2 中间件的体验

```
from django.utils.deprecation import MiddlewareMixin

class M1(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 如果方法没有返回值，(返回None)，可以继续往后走
        # 如果有返回值， HttpResponse, render, redirect
        print('M1: 进来了')
  
    def process_response(self, request, response):
        print('M1: 离开了')
        return response
  
class M2(MiddlewareMixin):
    """ 中间件2 """

    def process_request(self, request):
        print('M2: 进来了')
  
    def process_response(self, request, response):
        print('M2: 离开了')
        return response
```

- 应用中间件

  ```
  MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
      # 中间件，谁在前执行谁，views执行前需要穿过中间件(request)，返回给客户端(resonpse)也需要经过中间件
      # 栈规则
      'app01.middleware.auth.M1',
      'app01.middleware.auth.M2',
  ]
  ```

### 13.3 中间件校验

```python
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """
    def process_request(self, request):
        # 如果方法没有返回值，(返回None)，可以继续往后走
        # 如果有返回值， HttpResponse, render, redirect

        #  0. 排除不需要登陆就能访问的页面
        # request.path_info 获取当前用户请求的URL, /login/
        if request.path_info == "/login/":
            return

        # 1. 读取当前访问的用户session信息，如果能读到，说明已登录，可以继续往后走
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 2. 没有登陆过
        # return HttpResponse("未登录")
        return redirect('/login/')
  
    def process_response(self, request, response):
        print('M1: 离开了')
        return response
  
```

- setting.py 注册，应用中间件

  ```
  MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
      # 中间件，谁在前执行谁，views执行前需要穿过中间件(request)，返回给客户端(resonpse)也需要经过中间件

      'app01.middleware.auth.AuthMiddleware',
  ]
  ```

### 13.4 注销

### 13.5 当前用户


## 14.图片验证码

### 14.1 生成图片

```
pip install pillow
```

```
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter 
def check_code(width=120, height=30, char_length=5, font_file='day2\\Monaco.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')
 
    def rndChar():
        """
        生成随机字母   
        :return:
        """
        return chr(random.randint(65, 90))
 
    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
 
    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())
 
    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
 
    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())
 
    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
 
        draw.line((x1, y1, x2, y2), fill=rndColor())
 
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img,''.join(code)
 
 
if __name__ == '__main__':
    # 1. 直接打开
    img,code = check_code()
    # img.show()
    print(code)
 
    # 2. 写入文件
    # img,code = check_code()
    with open('code.png','wb') as f:
        img.save(f, format='png')
 
    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()
 
    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()
 
    pass
```

## 15.Ajax请求

浏览器向网站发送请求时：URL和表单的形式提交

- GET
- POST
  特点： 页面刷新

除此之外，也可以基于Ajax向后台发送请求(偷偷的发送请求)。

- 依赖jQuery
- 便携ajax代码

  ```
  $.ajax(
  	url:"发送的地址",
  	type:"post",
  	data:{
  		n1:123,
  		n2:456
  	},
  	success:function(res){
  		console.log(res);
  	}
  )
  ```

### 15.1 request.get请求

```
{% block js %}
    <!-- <script>
        $(function(){
            $(".btn").click(function(){
                alert("你点击了按钮");
            })
        })
    </script> -->
    <script type="text/javascript">
        function clickMe(){
            // console.log("点击了按钮")
            $.ajax({
                url: "/task/ajax/",
                type: "get",
                data: {
                    n1: 123,
                    n2: 456
                },
                success: function(res) {
                    console.log(res);// 终端打印response
                }

            })
        }
    </script>

{% endblock %}
```

```
def  task_ajax(request):
    """ 测试ajax请求 """
    print(request.GET) # <QueryDict: {'n1': ['123'], 'n2': ['456']}>
    return HttpResponse("成功了")
```

### 15.2 POST请求

```

```

```
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt # 免除scrf_token验证，ajax post
def  task_ajax(request):
    """ 测试ajax请求 """
    print(request.GET) # <QueryDict: {'n1': ['123'], 'n2': ['456']}>
    return HttpResponse("成功了")
```
