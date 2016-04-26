# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from eweb.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
# Create your views here.


from databaselib import cart_base
import json

@csrf_exempt
def homepage(request):
    """
    进入商城主页面,包含导航栏，搜索栏购物车，推荐，热卖产品，过滤字段排序，和商品
    """
    #print request.session
    print id(request)
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
def goodsinfo(request, product_id):
    """
    进入商品详情页面(继承homepage页面)
    """
    return render(request, 'eweb/goods.html')



@csrf_exempt
def order(request):
    """
    商品详情页的购买，点击进入我的购物车页面,
    直接点击支付按钮进入填写订单，确定支付
    """
    return render(request, 'eweb/cart.html')


def personal(request):
    '''
    个人中心页面
    '''
    return render(request, 'eweb/personal.html')



#购物车部分

@csrf_exempt
def cart(request):
    """
    进入我的购物车页面,没登陆和登陆都能看到购物车(继承homepage页面)
    """
    #return render(request, 'eweb/cart.html')
    #Get请求
    if request.method == 'GET':
        return GetResponse(request);
    elif request.method == 'POST':
        #Post请求用于处理订单提交，数据修改等
        ##
        return PostResponse(request);
    #return render(request, 'eweb/cart.html')

def GetResponse(request):
    """
    GetResponse 函数返回购物车页面
    """
    print request.GET
    if request.GET.get("commend") == "GetCartItems":
        itemlist = cart_base.GetItemList(request)
        displaylist = cart_base.GetItemsDetailForDisplay(*itemlist)
        cart = {
                "Contents":displaylist,
                "Count":len(displaylist),
        }
        return JsonResponse(cart)

    else:
        return render(request, 'eweb/cart.html')


def PostResponse(request):
    #1对购物车中商品的改动事件
    if request.POST.get("commend") == "UpdateCartItem":
        print "OK!"

        itemid = request.POST.get("ItemId")
        count = int(request.POST.get("ItemCount"))
        item = (itemid, count)
        cart_base.SetItemsInCart(request, item)
    elif request.POST.get("commend") == "Settle":
        print "Settle"
        print request.POST
        items = json.loads(request.POST.get("itemlist"))
        if cart_base.GenerateTempOrder(request, *items) == False:
            return JsonResponse({"Status":"Error","Reason":"结算失败，无货"})
        else:
            return JsonResponse({"Status":"Success"})


    #2提交事件
    ##1）提交会生成一个shipping_list，表示提交的商品
    ##2）核对登录与否：
        ###如果没有登录，进入登录界面进行登录
        ###如果已经登录，那么下一步
    ##3）后台根据shipping_list进行商品核对，
        ###如果核对成功，那么生成订单，并且删除购物车中的item，然后跳转到订单页面
        ###如果核对失败，进行失败处理（比如修改购物车中item的信息），然后返回购物页面，并且显示失败信息


@login_required
def cartstep2(request):
    '''
    购物付款流程2
    '''
    if request.method == "GET":
        #获得零时订单，如果没有零时订单，那么返回到购物车
        tempOrder = cart_base.GetTempOrder(request)
        displaylist = cart_base.GetItemsDetailForDisplay(*tempOrder)
        total = 0
        for i in range(len(displaylist)):
            displaylist[i]["Cost"] = float(displaylist[i]["Price"]) * float(displaylist[i]["Count"])
            total +=displaylist[i]["Cost"]
        cart = {
                "Contents":displaylist,
                "Total":total,
        }
        return render(request, 'eweb/cartstep2.html', cart)
        #如果有零时订单，那么返回
    elif request.method == "POST":
        print request
        if cart_base.SubmitOrder(request) == False:
            return HttpResponseRedirect(request, "/eweb/cart/")
        else:
            return render(request, 'eweb/cartstep3.html')

@login_required
def cartstep3(request):
    '''
    购物付款流程3
    '''
    return render(request, 'eweb/cartstep3.html')
