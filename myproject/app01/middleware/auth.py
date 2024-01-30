from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect

class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """
    def process_request(self, request):
        # 如果方法没有返回值，(返回None)，可以继续往后走
        # 如果有返回值， HttpResponse, render, redirect

        #  0. 排除不需要登陆就能访问的页面
        # request.path_info 获取当前用户请求的URL, /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return

        # 1. 读取当前访问的用户session信息，如果能读到，说明已登录，可以继续往后走
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 2. 没有登陆过
        # return HttpResponse("未登录")
        return redirect('/login/')
    
    # def process_response(self, request, response):
    #     print('M1: 离开了')
    #     return response
    