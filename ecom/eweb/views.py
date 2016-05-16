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
from databaselib import cart_base, db_service
import json


@csrf_exempt
def homepage(request):
    """
    进入商城主页面,包含导航栏，搜索栏购物车，推荐，热卖产品，过滤字段排序，和商品
    """
    brand_name = []
    feature_list = []
    product_list = []
    brand_list = db_service.GetAllBrandName()
    for brand in brand_list:
        brandname = brand_list[brand]
        brand_name.append(brandname)
    # print brand_name

    feature_list1 = db_service.GetAllFeatureName()
    for feature in feature_list1:
        feature_list.append(feature_list1[feature])
    type_list = []
    type_list1 = db_service.GetAllProdTypeName()
    for type1 in type_list1:
        type_list.append(type_list1[type1])

    # 三个过滤条件列表去重
    brand_name = set(brand_name)
    featuer_list = set(feature_list)
    type_list = set(type_list)
    # 热销产品列表
    hot_list = []
    # 推荐产品列表
    commend_list = []
    hot_list1 = Product.objects.filter(is_hot=True)
    print '**hot_list1**'
    print len(hot_list1)
    print '**hot_list1**'
    for one in hot_list1:
        hot_List = {}
        hot_List['id']=one.product_id
        hot_List['name'] = one.name
        print '**hot_List["name"]**'
        print hot_List["name"]
        print '**hot_List["name"]**'
        img_temp = Img.objects.filter(product=one)
        for a in img_temp:
            hot_List['img'] = str(a.url)
            print '**hot_List["img"]**'
            print hot_List["img"]
            print '**hot_List["img"]**'
        sku_tmep = Sku.objects.filter(product=one)
        for one1 in sku_tmep:
            hot_List['price'] = one1.price
            hot_list.append(hot_List)
        # 取出四件推荐商品
    hot_list = hot_list[0:4]
    print '**hot_list.len**'
    print len(hot_list)
    print '**hot_list.len**'
# sui ji xian shi  16 ge shangpin
    Product_list1 = Product.objects.order_by('product_id')[:16]
    for a in Product_list1:
        Product_dic = {}
        Product_dic['id'] = a.product_id
        print '****id:' + str(Product_dic['id'])
        Product_dic['name'] = a.name
        temp = Img.objects.filter(product=a)
        print "********************7777*"
        for a1 in temp:
            Product_dic['img'] = str(a1.url)
        temp1 = Sku.objects.filter(product=a)
        for a2 in temp1:
            Product_dic['price'] = a2.price
            product_list.append(Product_dic)

    commend_list1 = Product.objects.filter(is_commend=True)
    for one in commend_list1:
        commend_List = {}
        commend_List ['id'] = one.product_id
        commend_List['name'] = one.name
        img_temp = Img.objects.filter(product=one)
        for a in img_temp:
            commend_List['img'] = str(a.url)
        sku_temp = Sku.objects.filter(product=one)
        for one1 in sku_temp:
            commend_List['price'] = one1.price
            commend_list.append(commend_List)
    commend_list = commend_list[0:4]
    print '**commend_list.len**'
    print len(commend_list)
    print '**commend_list.len**'
    return render(request, 'homepage.html', {'product_list': product_list, 'commend_list': commend_list, 'hot_list': hot_list, 'type_list': type_list, 'feature_list': feature_list, 'brand_name': brand_name})

BRAND_LIST = {}
A_BRAND = set()
B_BRAND = set()
C_BRAND = set()
BRAND_SELECT = {}
BRAND_LAST = ''
FEATURE_LAST = ''
TYPE_LAST = ''


@csrf_exempt
def showproduct(request):
    """
    过滤条件,ajax刷新商品信息
    """
    # color = request.GET.get('color')
    # number = request.GET.get('number')
    # name = '{}_{}'.format(color, number)
    # result_list = filter(lambda x: x.startswith(name), PICS)
    global BRAND_LIST
    global A_BRAND
    global B_BRAND
    global C_BRAND
    global BRAND_LAST
    global FEATURE_LAST
    global TYPE_LAST
    global BRAND_SELECT

    brandname_set = set()
    feature_set = set()
    type_set = set()
    # BRAND_SELECT={'brand':'all','type':'all','featuer':'all'}
    brandname_list1 = db_server.GetAllBrandName()
    for brand in brandname_list1:
        A_BRAND.add(brandname_list1[brand])
    feature_list1 = db_server.GetAllFeatureName()
    for feature in feature_list1:
        B_BRAND.add(feature_list1[feature])
    type_list1 = db_server.GetAllProdTypeName()
    for type1 in type_list1:
        C_BRAND.add(type_list1[type1])
    a = request.GET.get('a')
    a = a.encode('utf8')
    if a in A_BRAND:
        temp_set = set()
        temp_set.add(a)
        BRAND_LAST = A_BRAND & temp_set
    elif a in B_BRAND:
        temp_set = set()
        temp_set.add(a)
        FEATURE_LAST = B_BRAND & temp_set
    elif a in C_BRAND:
        temp_set = set()
        temp_set.add(a)
        TYPE_LAST = C_BRAND & temp_set
    else:
        if a == 'all1':
            BRAND_LAST = set()
        elif a == 'all2':
            TYPE_LAST = set()
        else:
            FEATURE_LAST = set()

    print '---------------BRAND---------------------'
    print list(BRAND_LAST)
    print list(FEATURE_LAST)
    print list(TYPE_LAST)
    print '----------------BRAND---------------------'
    product_list = []
    if len(BRAND_LAST) == 0 and len(FEATURE_LAST) == 0 and len(TYPE_LAST) == 0:
        Product_list1 = Product.objects.order_by('?')[:16]
        for a in Product_list1:
            Product_dic = {}
            Product_dic['id'] = a.product_id
            print '****id:' + str(Product_dic['id'])
            Product_dic['name'] = a.name
            temp = Img.objects.filter(product=a)
            print "********************7777*"
            for a1 in temp:
                Product_dic['img'] = str(a1.url)
            temp1 = Sku.objects.filter(product=a)
            for a2 in temp1:
                Product_dic['price'] = a2.price
                product_list.append(Product_dic)
                return product_list

    elif len(BRAND_LAST) == 1 and len(FEATURE_LAST) == 0 and len(TYPE_LAST) == 0:
        for i in BRAND_LAST:
            Product_Brand = Brand.objects.filter(name=str(i))
            for pb in Product_Brand:
                Product_b = Product.objects.filter(brand=pb)
                for a in Product_b:
                    Product_dic = {}
                    Product_dic['id'] = a.product_id
                    print '****id:' + str(Product_dic['id'])
                    Product_dic['name'] = a.name
                    temp = Img.objects.filter(product=a)
                    print "********************7777*"
                    for a1 in temp:
                        Product_dic['img'] = str(a1.url)
                    temp1 = Sku.objects.filter(product=a)
                    for a2 in temp1:
                        Product_dic['price'] = a2.price
                        product_list.append(Product_dic)
                        return product_list

    elif len(BRAND_LAST) == 1 and len(FEATURE_LAST) == 1 and len(TYPE_LAST) == 0:
        for i in BRAND_LAST:
            Product_Brand = Brand.objects.filter(name=str(i))
        for j in FEATURE_LAST:
            Feature_Brand = Productfeature.objects.filter(name=str(j))
        for pb in Product_Brand:
            for pf in Feature_Brand:
                Product_b = Product.objects.filter(brand=pb, features=pf)
                for a in Product_b:
                    Product_dic = {}
                    Product_dic['id'] = a.product_id
                    print '****id:' + str(Product_dic['id'])
                    Product_dic['name'] = a.name
                    temp = Img.objects.filter(product=a)
                    print "********************7777*"
                    for a1 in temp:
                        Product_dic['img'] = str(a1.url)
                    temp1 = Sku.objects.filter(product=a)
                    for a2 in temp1:
                        Product_dic['price'] = a2.price
                        product_list.append(Product_dic)
                        return product_list

    elif len(BRAND_LAST) == 1 and len(FEATURE_LAST) == 1 and len(TYPE_LAST) == 1:
        for i in BRAND_LAST:
            Product_Brand = Brand.objects.filter(name=str(i))
        for j in FEATURE_LAST:
            Feature_Brand = Productfeature.objects.filter(name=str(j))
        for k in TYPE_LAST:
            Type_Brand = Producttype.objects.filter(name=str(k))
        for pb in Product_Brand:
            for pf in Feature_Brand:
                for pt in Type_Brand:
                    Product_b = Product.objects.filter(
                        brand=pb, features=pf, producttype=pt)
                    for a in Product_b:
                        Product_dic = {}
                        Product_dic['id'] = a.product_id
                        print '****id:' + str(Product_dic['id'])
                        Product_dic['name'] = a.name
                        temp = Img.objects.filter(product=a)
                        print "********************7777*"
                        for a1 in temp:
                            Product_dic['img'] = str(a1.url)
                        temp1 = Sku.objects.filter(product=a)
                        for a2 in temp1:
                            Product_dic['price'] = a2.price
                            product_list.append(Product_dic)
                            return product_list

    elif len(BRAND_LAST) == 1 and len(FEATURE_LAST) == 0 and len(TYPE_LAST) == 1:
        for i in BRAND_LAST:
            Product_Brand = Brand.objects.filter(name=str(i))
        for j in TYPE_LAST:
            Type_Brand = Producttype.objects.filter(name=str(j))
        for pb in Product_Brand:
            for pt in Type_Brand:
                Product_b = Product.objects.filter(brand=pb, producttype=pt)
                for a in Product_b:
                    Product_dic = {}
                    Product_dic['id'] = a.product_id
                    print '****id:' + str(Product_dic['id'])
                    Product_dic['name'] = a.name
                    temp = Img.objects.filter(product=a)
                    print "********************7777*"
                    for a1 in temp:
                        Product_dic['img'] = str(a1.url)
                    temp1 = Sku.objects.filter(product=a)
                    for a2 in temp1:
                        Product_dic['price'] = a2.price
                        product_list.append(Product_dic)
                        return product_list

    elif len(BRAND_LAST) == 0 and len(FEATURE_LAST) == 1 and len(TYPE_LAST) == 1:
        for i in FEATURE_LAST:
            Feature_Brand = Productfeature.objects.filter(name=str(i))
        for j in TYPE_LAST:
            Type_Brand = Producttype.objects.filter(name=str(j))
        for pf in Feature_Brand:
            for pt in Type_Brand:
                Product_b = Product.objects.filter(features=pf, producttype=pt)
                for a in Product_b:
                    Product_dic = {}
                    Product_dic['id'] = a.product_id
                    print '****id:' + str(Product_dic['id'])
                    Product_dic['name'] = a.name
                    temp = Img.objects.filter(product=a)
                    print "********************7777*"
                    for a1 in temp:
                        Product_dic['img'] = str(a1.url)
                    temp1 = Sku.objects.filter(product=a)
                    for a2 in temp1:
                        Product_dic['price'] = a2.price
                        product_list.append(Product_dic)
                        return product_list
    elif len(BRAND_LAST) == 0 and len(FEATURE_LAST) == 1 and len(TYPE_LAST) == 0:
        for i in FEATURE_LAST:
            Feature_Brand = Productfeature.objects.filter(name=str(i))
            for pf in Feature_Brand:
                Product_b = Product.objects.filter(features=pf)
                for a in Product_b:
                    Product_dic = {}
                    Product_dic['id'] = a.product_id
                    print '****id:' + str(Product_dic['id'])
                    Product_dic['name'] = a.name
                    temp = Img.objects.filter(product=a)
                    print "********************7777*"
                    for a1 in temp:
                        Product_dic['img'] = str(a1.url)
                    temp1 = Sku.objects.filter(product=a)
                    for a2 in temp1:
                        Product_dic['price'] = a2.price
                        product_list.append(Product_dic)
                        return product_list
    elif len(BRAND_LAST) == 0 and len(FEATURE_LAST) == 0 and len(TYPE_LAST) == 1:
        for i in TYPE_LAST:
            Type_Brand = Producttype.objects.filter(name=str(i))
            for pt in Type_Brand:
                Product_b = Product.objects.filter(features=pt)
                for a in Product_b:
                    Product_dic = {}
                    Product_dic['id'] = a.product_id
                    print '****id:' + str(Product_dic['id'])
                    Product_dic['name'] = a.name
                    temp = Img.objects.filter(product=a)
                    print "********************7777*"
                    for a1 in temp:
                        Product_dic['img'] = str(a1.url)
                    temp1 = Sku.objects.filter(product=a)
                    for a2 in temp1:
                        Product_dic['price'] = a2.price
                        product_list.append(Product_dic)
                        return product_list

    print '****result******'
    for one in product_list:
        print one['name']
    print '*****result******'
    return HttpResponse(json.dumps(product_list), content_type='application/json')


@csrf_exempt
# 分页显示
def getproductPosts(rq):
    try:
        curPage = int(rq.GET.get('curPage', '1'))
        allPage = int(rq.GET.get('allPage', '1'))
        pageType = str(rq.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''
    # 判断点击了[上一页]还是[下一页]
    if pageType == 'pageDown':

        curPage += 1

    elif pageType == 'pageUp':

        curPage -= 1
    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    posts = BlogPost.objects.all()[startPos:endPos]

    if curPage == 1 and allPage == 1:  # 标记1
        allPostCounts = BlogPost.objects.count()
        allPage = allPostCounts / ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    return render(rq, "homepage.html", {'posts': posts, 'allPage': allPage, 'curPage': curPage})


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
    #
    prodInfo = db_service.GetProductInfo(product_id, "ProdTypeId", "BrandID", "Name", "Weight",
                                         "Package", "New", "Hot", "Commend", "DescImage", "Features", "Colors", "Sizes", "CreateTime")
    prodInfo["ProductId"] = product_id
    print prodInfo["DescImage"]
    brandInfo = db_service.GetBrandInfo(
        prodInfo["BrandID"], "Name", "Desc", "LogoUrl")
    inventory = db_service.GetProductInventory(product_id)
    inventList = []
    colorList = []
    sizeList = []
    for inventid in inventory:
        item = db_service.GetInventorInfo(
            inventid, "Color", "Size", "Price", "Stock", "InvImg", "DeliveFee")
        if int(item["Stock"]) <= 0:
            continue
        item["InventId"] = inventid
        inventList.append(item)
        colorList.append(item["Color"])
        sizeList.append(item["Size"])
        print item["InvImg"]

    colorList = list(set(colorList))

    i = 0
    colors = []
    for colorname in colorList:
        color = {}
        color["Name"] = colorname
        color["ID"] = str(i)
        i += 1
        colors.append(color)

    sizeSet = set(sizeList)
    sizeList = ["S", "M", "L", "XL", "XXL"]
    i = 0
    sizes = []
    for sizename in sizeList:
        if sizename in sizeSet:
            size = {}
            size["Name"] = sizename
            size["ID"] = str(i)
            i += 1
            sizes.append(size)

    contents = {
        "ProductDict": prodInfo,
        "BrandDict": brandInfo,
        "InventList": inventList,
        "ColorList": colors,
        "SizeList": sizes
    }
    return render(request, 'eweb/goods.html', contents)


def personal(request):
    '''
    个人中心页面
    '''
    return render(request, 'eweb/personal.html')


# 购物车部分

@csrf_exempt
def cart(request):
    """
    进入我的购物车页面,没登陆和登陆都能看到购物车(继承homepage页面)
    """
    # return render(request, 'eweb/cart.html')
    # Get请求
    if request.method == 'GET':
        return GetResponse(request)
    elif request.method == 'POST':
        # Post请求用于处理订单提交，数据修改等
        ##
        return PostResponse(request)
    # return render(request, 'eweb/cart.html')


def GetResponse(request):
    """
    GetResponse 函数返回购物车页面
    """
    print request.GET
    if request.GET.get("commend") == "GetCartItems":
        itemlist = cart_base.GetItemList(request)
        displaylist = cart_base.GetItemsDetailForDisplay(*itemlist)
        cart = {
            "Contents": displaylist,
            "Count": len(displaylist),
        }
        return JsonResponse(cart)

    else:
        return render(request, 'eweb/cart.html')


def PostResponse(request):
    # 1对购物车中商品的改动事件
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
            return JsonResponse({"Status": "Error", "Reason": "结算失败，无货"})
        else:
            return JsonResponse({"Status": "Success"})
    elif request.POST.get("commend") == "AddItem":
        print "AddItem"
        print request.POST
        count = int(request.POST["count"])
        productid = request.POST["id"]
        if count == None or productid == None or count <= 0:
            return JsonResponse({"Status": "Error"})
        cart_base.ModifyItemsInCart(request, (productid, count))
        return JsonResponse({"Status": "Success"})

    # 2提交事件
    # 1）提交会生成一个shipping_list，表示提交的商品
    # 2）核对登录与否：
        # 如果没有登录，进入登录界面进行登录
        # 如果已经登录，那么下一步
    # 3）后台根据shipping_list进行商品核对，
        # 如果核对成功，那么生成订单，并且删除购物车中的item，然后跳转到订单页面
        # 如果核对失败，进行失败处理（比如修改购物车中item的信息），然后返回购物页面，并且显示失败信息


@login_required
def cartstep2(request):
    '''
    购物付款流程2
    '''
    if request.method == "GET":
        # 获得零时订单，如果没有零时订单，那么返回到购物车
        tempOrder = cart_base.GetTempOrder(request)
        displaylist = cart_base.GetItemsDetailForDisplay(*tempOrder)
        total = 0
        for i in range(len(displaylist)):
            displaylist[i]["Cost"] = float(
                displaylist[i]["Price"]) * float(displaylist[i]["Count"])
            total += displaylist[i]["Cost"]
        cart = {
            "Contents": displaylist,
            "Total": total,
        }
        return render(request, 'eweb/cartstep2.html', cart)
        # 如果有零时订单，那么返回
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
