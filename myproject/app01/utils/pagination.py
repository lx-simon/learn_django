'''
自定义的分页组件
    以后需要使用这个分页组件，你需要做以下这几件事情
在视图函数中:
def pretty_list(request):
    
    # 1.根据自己的情况筛选自己的数据
    queryset = models.PrettyNum.objects.all()
    # 2.实例化分页对象
    page_object = Pagination(request, queryset)

    context = {"search_data": search_data,
               'queryset': page_object.queryset, # 分完页的数据
               "page_string":page_object.html(), # 页面
            }
    return render(request, 'pretty_list.html', context)
在HTML页面中:
{% for obj in queryset %}
    {{ obj.xxx }}
{% endfor %}
<ul class="pagination">
    {{ page_string }}
</ul>

'''
from django.utils.safestring import mark_safe
class Pagination(object):
    def __init__(self, request, queryset, page_size=10, page_param="page", plus=5):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他分页）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/list/?page=2
        :param plus: 显示当前页面的前5页，后5页
        :return:
        """

        import copy
        from django.http.request import QueryDict
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        # query_dict.setlist("page", [])
        # url参数page设置并保留当前存在的其它参数
        self.query_dict = query_dict
        self.page_param = page_param
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        # print(page,type(page))
        else:
            page = 1
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        # 1.根据用户想访问的页面，计算出值
        self.queryset = queryset[self.start:self.end]

        # 数据总条数
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div: # 有余数，多一页
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，显示当前页面的前5页，后5页

        if self.total_page_count <= 2*self.plus:
            # 数据库数量比较少，没达到11页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中数据数据量多, > 11页
            ## 当前页<5时
            if self.page <= self.plus:
                start_page = 1
                end_page = 2*self.plus+1
            else:
                # 当前页面>5
                ## 当前页面+5>总页面
                if (self.page+self.plus)>self.total_page_count:
                    start_page = self.total_page_count -2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page-self.plus
                    end_page = self.page+self.plus
        

        # 页码
        page_str_list = []        

        # 首页
        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{0}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = '<li><a href="?{0}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li class="disabled"><a href="?{0}" aria-label="Previous"><span aria-hidden="true">«</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page,end_page+1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:  
                ele = '<li class="active"><a href="?{0}">{1}</a></li>'.format(self.query_dict.urlencode(),i)
            else:
                ele = '<li><a href="?{0}">{1}</a></li>'.format(self.query_dict.urlencode(),i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])
            next = '<li><a href="?{0}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li class="disabled"><a href="?{0}" aria-label="Next"><span aria-hidden="true">»</span></a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{0}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = '''
        <li>
            <form stype="float: left;margin-left: -1px" method="get">
                <input name="page" 
                    style="position: relative;float: left;display: inline-block;width: 80px;border-radius: 0;"
                    type="text" class="form-control" placeholder="页码">
                <span class="input-group-btn">
                    <button class="btn btn-default" type="submit">跳转</button>
                </span>
            </form>
        </li>
        '''
        page_str_list.append(search_string)

        page_string = mark_safe("".join(page_str_list))
        return page_string