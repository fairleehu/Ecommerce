# coding=utf-8
import time
import db_service
from django.contrib.auth.decorators import login_required
from ecom.settings import MEDIA_URL


def GetItemList(request):
    """
    获得用户的购物车列表信息
    返回[(itemA, countA, timeA),(itemB, countB, timeB), ......]
    """
    itemlist = {}
    items = []
    login_statue = request.user.is_authenticated()
    # print login_statue
    if login_statue == True:
        username = request.user.get_username()
        # 如果登录，对redis中的shoppingCart进行操作
        itemsCount = db_service.GetItemsCountInCart(username)
        itemsAddTime = db_service.GetItemsAddTimeInCart(username)
        for key in itemsCount.keys():
            item = (key, itemsCount[key], itemsAddTime[key])
            items.append(item)
    else:
        # 如果没有登录，对cookie进行操作
        offlineCart = request.session.get('shoppingCart')
        if offlineCart != None:
            for key in offlineCart.keys():
                if offlineCart[key] < 0:
                    del offlineCart[key]
                else:
                    item = (key, offlineCart[key], int(time.time()))
                    items.append(item)

            # print "shoppingCart" + str(request.session.get('shoppingCart'))
    # TEST TODO
    #items = [(1, 3, int(time.time())-12), (2, 5, int(time.time()))]
    return items


def ModifyItemsInCart(request, *items):
    """
    用来增减商品的数量,如果商品数量小于等于0会删除商品
    """
    login_statue = request.user.is_authenticated()
    # print login_statue
    if login_statue == True:
        username = request.user.get_username()
        # 如果登录，对redis中的shoppingCart进行操作
        for item in items:
            db_service.ModifyItemInDBCart(username, item)
    else:
        # 如果没有登录，对cookie进行操作
        offlineCart = request.session.get('shoppingCart')
        if offlineCart == None:
            offlineCart = {}

        for item in items:
            count = offlineCart.get(item[0])
            if count == None:
                count = 0
            offlineCart[item[0]] = int(count) + int(item[1])
            if offlineCart[item[0]] <= 0:
                del offlineCart[item[0]]
        request.session['shoppingCart'] = offlineCart
        # print "shoppingCart" + str(request.session.get('shoppingCart'))
    return True


def SetItemsInCart(request, *items):
    """
    用来设置商品的数量，如果商品数量小于等于0会删除商品
    """
    login_statue = request.user.is_authenticated()
    # print login_statue
    if login_statue == True:
        username = request.user.get_username()
        for item in items:
            db_service.SetItemInDBCart(username, item)
    else:
        offlineCart = request.session.get('shoppingCart')
        if offlineCart == None:
            request.session['shoppingCart'] = {}
            offlineCart = request.session.get('shoppingCart')

        for item in items:
            offlineCart[item[0]] = int(item[1])
            if offlineCart[item[0]] < 0:
                del offlineCart[item[0]]

        request.session['shoppingCart'] = offlineCart
        # print "shoppingCart" + str(request.session.get('shoppingCart'))
    return True


def GenerateTempOrder(request, *itemlist):
    tempOrder = []
    items = []
    Check = True
    for item in itemlist:
        # print item
        items.append((item["ID"], int(item["COUNT"])))
        if int(item["COUNT"]) > 0:
            tempOrder.append(item["ID"])
    SetItemsInCart(request, *items)

    # 核对库存
    for item in items:
        if item[1] > 0:
            if db_service.CheckInventoryStock(item[0], item[1]) == False:
                Check = False
                break
    if Check == False:
        return False
    else:
        return CreateTempOrder(request, tempOrder)


def CreateTempOrder(request, tempOrder):
    login_statue = request.user.is_authenticated()
    if login_statue == True:
        username = request.user.get_username()
        db_service.CreateTempOrder(username, tempOrder)
    else:
        request.session["tempOrder"] = tempOrder
    return True


def GetTempOrder(request):
    username = request.user.get_username()
    return db_service.GetTempOrder(username)


def GetItemsDetailForDisplay(*itemlist):
    """
    获得用以在购物车中显示的商品信息
    @input (itemA, countA, timeA),(itemB, countB, timeB), ......
    @ret 返回一个项目字典的list
    对于返回的显示信息有{
        "ItemID":,
        "ProductID":,           #用于回调到产品页
        "Name":,
        "Color":,
        "Size":,
        "Price":,
        "Image":,
        "DelivFee"
        "Stock":,
        "Count":,
        "AddTime":,
    }
    """
    # TODO 错误处理
    retList = []
    for item in itemlist:
        itemDetail = {}
        itemDetail["ItemID"] = item[0]
        invetInfo = db_service.GetInventorInfo(
            item[0], "ProdectID", "Color", "Size", "Price", "DeliveFee", "Stock", "InvImg")
        itemDetail["ProductID"] = invetInfo["ProdectID"]
        itemDetail["Name"] = db_service.GetProductInfo(
            invetInfo["ProdectID"], "Name").get("Name")
        itemDetail["Color"] = invetInfo["Color"]
        itemDetail["Size"] = invetInfo["Size"]
        itemDetail["Price"] = invetInfo["Price"]
        itemDetail["Image"] = MEDIA_URL + invetInfo["InvImg"]
        itemDetail["DelivFee"] = invetInfo["DeliveFee"]
        itemDetail["Stock"] = invetInfo["Stock"]
        itemDetail["Count"] = item[1]
        itemDetail["AddTime"] = item[2]
        retList.append(itemDetail)
    return retList


@login_required
def MergeAfterLogin(request):
    """
    在用户登录后
    将cookie中的商品加到shoppingCart中
    """
    # SetCSessionId(request)
    offlineCart = request.session.pop('shoppingCart')
    if offlineCart != None:
        # 合并商品
        items = []
        # 选出cookies中数量大于0的商品
        for key in offlineCart.keys():
            if offlineCart[key] > 0:
                item = (key, offlineCart[key])
                items.append(item)
        SetItemInDBCart(request, items)
    tempOrder = request.session.pop('tempOrder')
    if tempOrder != None:
        CreateTempOrder(request, tempOrder)
    return True


@login_required
def SubmitOrder(request):
    """
    核对库存，如果核对成功，那么返回True，如果核对失败，那么返回False
    """
    username = request.user.get_username()
    tempOrder = db_service.GetTempOrder(username)
    if len(tempOrder) == 0:
        return False
    items = []
    for item in tempOrder:
        items.append((item[0], int(item[1])))

    if db_service.ChangeStock(items) == False:
        return False

    db_service.CreateUnpayedOrder(username, items)
    removeList = []
    for item in items:
        removeList.append((item[0], -item[1]))
    ModifyItemsInCart(request, *removeList)
    # 如果2小时内未完成支付（注意，时间必须小于redis中库存的lifetime），此未提交订单会作废（用守护进程进行处理），作废后订单中的数量会加回到redis中
    return True

# TODO 删除


def GetUserId(request):
    """
    获得userid
    """
    csessionid = request.session.get('CssID')
    if csessionid != None:
        userid = db_service.GetUserId(csessionid)
    else:
        userid = None
    return userid

# TODO 删除


@login_required
def SetCSessionId(request):
    """
    设置CSessionId
    """
    username = request.user.get_username()
    csessionid = db_service.CreateNewSession(username)
    request.session['CssID'] = csessionid
    return True
