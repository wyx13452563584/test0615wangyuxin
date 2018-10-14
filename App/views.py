from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from App.models import HomeWheel, movies, UserModel


def index(request):
    return HttpResponse("test")

def home(request):
    is_login = False
    user_id = request.session.get('user_id')
    wheels =HomeWheel.objects.all()
    movies_list =movies.objects.all()

    data = {
        'title': '首页',
        "wheels": wheels,
        "movies":movies_list,
        "is_login": is_login,
    }

    if user_id:
        try:
            user = UserModel.objects.get(pk=user_id)
            is_login = True
            data['is_login'] = is_login
            data['user_icon'] = '/static/upload/' + user.u_icon.url
            data['username'] = user.u_name
        except Exception as e:
            print(str(e))
        return render(request, 'home_logined.html', context=data)
    else:
        return render(request, 'home.html', context=data)







def user_register(request):
    if request.method == "GET":
        data = {
            "title": '用户注册',
        }
        return render(request, 'register.html', context=data)

    elif request.method == "POST":

        u_name = request.POST.get("u_name")
        u_email = request.POST.get("u_email")
        u_password = request.POST.get("u_password")
        u_icon = request.FILES.get("u_icon")

        user = UserModel()
        user.u_name = u_name
        user.u_email = u_email
        user.u_icon = u_icon
        user.set_password(u_password)
        user.save()

        request.session['user_id'] = user.id
        return redirect(reverse('App:home'))
#
# def check_user(request):
#     u_name = request.GET.get("u_name")
#     users = UserModel.objects.filter(u_name=u_name)
#     data = {
#         'msg': 'ok',
#         'status': '200'
#     }
#     if users.exists():
#         # 告诉客户端用户存在
#         data['status'] = '901'
#         data['msg'] = "already exists"
#     else:
#         # 不存在，可以使用
#         data['status'] = '200'
#         # 可用
#         data['msg'] = 'avaliable'
#     return JsonResponse(data)


def user_login2(request):
    if request.method == "GET":
        msg = request.session.get('msg')
        data = {
            'title': '用户登录',
        }
        if msg:
            data['msg'] = msg

        return render(request, 'home.html', context=data)

    elif request.method == "POST":
        username = request.POST.get('u_name')
        password = request.POST.get('u_password')
        users = UserModel.objects.filter(u_name=username)
        if users.exists():
            user = users.first()
            if user.check_password(password):
                request.session['user_id'] = user.id
                return redirect(reverse('App:home'))
            else:
                request.session['msg'] = '密码错误'
                return redirect(reverse('App:login1'))
        else:
            request.session['msg'] = '用户名不存在'
            return redirect(reverse('App:login1'))

def user_login1(request):
    return render(request, 'login.html')


def user_collected(request):
    pass