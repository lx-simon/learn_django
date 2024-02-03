from django.shortcuts import render

def city_list(request):
    return render(request, 'city_list.html')