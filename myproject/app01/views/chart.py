from django.shortcuts import render
from django.http import JsonResponse

def chart_list(request):
    """ 数据统计页面 """
    return render(request, 'chart_list.html')

def chart_bar(request):
    """ 柱状图构造数据 """
    # 数据可以从数据库中获取

    legend = ['销量', "业绩"]
    
    data_list = [
                {
                "name": '销量',
                "type": 'bar',
                "data": [5, 20, 36, 10, 10, 20]
                },
                {
                "name": '业绩',
                "type": 'bar',
                "data": [52, 10, 32, 7, 110, 10]
                }
                ]
    data_type = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series': data_list,
            'xAxis': data_type,
        }
    }

    return JsonResponse(result)

def chart_pie(request):
    """ 饼状图构造数据 """
    # legend = ['销量', "业绩"]
    data_list = [
        { 'value': 1048,'name': 'Search Engine' },
        { 'value': 735, 'name': 'Direct' },
        { 'value': 580, 'name': 'Email' },
        { 'value': 484, 'name': 'Union Ads' },
        { 'value': 300, 'name': 'Video Ads' }
    ]
    result = {
        "status": True,
        "data": {
            # 'legend': legend,
            'data': data_list,
        }
    }

    return JsonResponse(result)

def chart_line(request):
    """ 折线图后台数据 """

    data_xaxis = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    data_label = ['销量', "业绩"]
    data = [
        {
        'data': [820, 932, 901, 934, 1290, 1330, 1320],
        'type': 'line',
        'smooth': True
        },
        {
        'data': [792, 232, 501, 534, 1590, 1230, 1920],
        'type': 'line',
        'smooth': True
        }
    ]
    result = {
        'data_xaxis': data_xaxis,
        'data_label': data_label,
        'data' : data
    }
    return JsonResponse({'status': True, 'data':result})

def chart_highcharts(request):
    ''' highcharts '''
    return render(request, 'highcharts.html')