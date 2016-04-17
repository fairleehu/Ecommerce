# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from eweb.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
# Create your views here.


@csrf_exempt
def homepage(request):
    """
    进入商城主页面,包含导航栏，搜索栏购物车，推荐，热卖产品，过滤字段排序，和商品 
    """
    return render(request, 'homepage.html')


@csrf_exempt
def login(request):
    """
    进入登陸界面，输入账号，密码
    """
    return render(request, 'eweb/loginpage.html')


@csrf_exempt
def register(request):
    """
    进入注册页面,用户名，密码,手机号
    """
    return render(request, 'eweb/registerpage.html')


@csrf_exempt
def goodsinfo(request):
    """
    进入商品详情页面(继承homepage页面)
    """
    return render(request, 'eweb/goods.html')


@csrf_exempt
def cart(request):
    """
    进入我的购物车页面,没登陆和登陆都能看到购物车(继承homepage页面)
    """
    return render(request, 'eweb/cart.html')

@csrf_exempt
def order(request):
    """
    商品详情页的购买，点击进入我的购物车页面,
    直接点击支付按钮进入填写订单，确定支付
    """
    return render(request, 'eweb/cart.html')