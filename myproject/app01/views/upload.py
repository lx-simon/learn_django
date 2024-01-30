from django.shortcuts import render, HttpResponse

def upload_list(request):
    if request.method == 'GET':
        return render(request, 'upload_list.html')
    # print(request.POST)
    # print(request.FILES)
    file_object = request.FILES.get('avatar')  # 获取上传的文件对象
    print(file_object.name) # 08f790529822720e0cf3722bfa821d46f21fbf097d82.jpeg
    
    for chunk in file_object.chunks():# 文件分块上传，也一点一点去读，chunk表示一块数据
        with open('a1.png', 'wb') as f:
            f.write(chunk)

    return HttpResponse(".....")