from django.shortcuts import render, HttpResponse, redirect
from app01.forms import LoginForm, RegisterForm
# Create your views here.
from app01 import models


def index(request):
    return render(request, 'index.html')


def login_decorate(func):
    # 登陆验证装饰器
    def wrap(request, *args, **kwargs):
        if request.session.get('subtitle') == kwargs.get('subtitle'):
            res = func(request, *args, **kwargs)
        else:
            res = redirect('/login/')
        return res

    return wrap


def login(request):
    '登录功能'
    if request.method == "GET":
        login_form = LoginForm(request)
        return render(request, 'login.html', {'login_form': login_form})
    else:
        login_form = LoginForm(request, request.POST)
        if login_form.is_valid():
            # 登录成功将subtitle写入session中
            subtitle = models.UserInfo.objects.filter(username=login_form.cleaned_data.get('username')).values(
                'blog__subtitle').first()
            request.session['subtitle'] = subtitle.get('blog__subtitle')
            # 登录成功返回到博客网主页
            if request.POST.get('remember_status', False):
                request.session.set_expiry(24 * 60 * 60 * 7)  # 设置一周免登陆
            else:
                request.session.set_expiry(2 * 60 * 60)  # 两个小时免登陆
            return redirect('/blog_mainpage/' + subtitle.get('blog__subtitle'))  # 如果redirect一个URL，该URL包含用户名即可
        return render(request, 'login.html', {'login_form': login_form})


import time


def register(request):
    '注册功能'
    if request.method == "GET":
        register_form = RegisterForm(request)
        return render(request, 'register.html', {'register_form': register_form})
    else:
        register_form = RegisterForm(request, request.POST, request.FILES)
        if register_form.is_valid():
            # 用户注册数据正确，将数据提交到数据库中
            user_info_dict = register_form.cleaned_data
            user_info_dict.pop('password2')
            user_info_dict.pop('check_code')
            if user_info_dict.get('avatar') == None:
                user_info_dict.pop('avatar')
            user_obj = models.UserInfo.objects.create(**user_info_dict)  # 将用户信息写入数据库
            # 默认开通博客
            title = user_info_dict.get('nickname')
            subtitle = user_info_dict.get('email').split('@')[0]
            theame = 'default'
            user = user_obj
            blog_dict = {}
            blog_dict['title'] = title
            blog_dict['subtitle'] = subtitle
            blog_dict['theame'] = theame
            blog_dict['user'] = user
            models.Blog.objects.create(**blog_dict)
            return redirect('/login/')
        return render(request, 'register.html', {'register_form': register_form})


from io import BytesIO
from app01.utlis.verfication_code import verfication_code


def check_code(request):
    '生成二维码'
    img, codes = verfication_code(font_file='static/font/kumo.ttf', font_size=30)
    f = BytesIO()
    img.save(f, 'png')
    img_data = f.getvalue()
    request.session['check_code'] = codes
    return HttpResponse(img_data)
