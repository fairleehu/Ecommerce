# coding=utf-8

import db_base
import uuid
import time
from eweb.models import *


"""
包含了对数据库的Server层的操作
封装应用层了对数据库的所有业务上的操作
通过db_base.py的接口实现
"""

Redis = db_base.RedisBase()

ITEM_UPDATETIME_MINNUMBER = 60 * 60 * 24


def NeedUpdateAddTime(itemOldTime):
    delta_time = long(time.time() - itemOldTime)
    if delta_time >= ITEM_UPDATETIME_MINNUMBER:
        return True
    else:
        return False

"""
购物车的操作
"""


def ModifyItemInDBCart(username, item):
    """
    用来修改数据库中的Cart，如果商品数量小于等于0会删除商品
    item为一个(itemID,number)的元组
    """
    cartItemCountKey = "CartIC:" + username
    cartAddTimeKey = "CartAT:" + username
    ret = Redis.Hincrby(cartItemCountKey, item[0], item[1])
    if ret <= 0:
        Redis.Hdel(cartItemCountKey, item[0])
        Redis.Hdel(cartAddTimeKey, item[0])
    else:
        itemOldTime = Redis.Hget(cartAddTimeKey, item[0])
        if itemOldTime == None or NeedUpdateAddTime(long(itemOldTime)):
            Redis.Hset(cartAddTimeKey, item[0], long(time.time()))
    return


def SetItemInDBCart(username, item):
    """
    用来修改数据库中的Cart，如果商品数量小于等于0会删除商品
    """
    # 商品加入的数量
    cartItemCountKey = "CartIC:" + username
    # 商品加入的时间，用于前端排序
    cartAddTimeKey = "CartAT:" + username
    if item[1] <= 0:
        Redis.Hdel(cartItemCountKey, item[0])
        Redis.Hdel(cartAddTimeKey, item[0])
    else:
        Redis.Hset(cartItemCountKey, item[0], item[1])
        itemOldTime = Redis.Hget(cartAddTimeKey, item[0])
        # 更新商品加入的时间
        if itemOldTime == None or NeedUpdateAddTime(long(itemOldTime)):
            Redis.Hset(cartAddTimeKey, item[0], long(time.time()))
    return


def GetItemsCountInCart(username):
    """
    返回购物车中所有的商品，以字典的形式
    """
    cartItemCountKey = "CartIC:" + username
    itemDict = Redis.Hgetall(cartItemCountKey)
    return itemDict


def GetItemsAddTimeInCart(username):
    """
    返回购物车商品添加的时间
    """
    cartAddTimeKey = "CartAT:" + username
    itemDict = Redis.Hgetall(cartAddTimeKey)
    return itemDict

TEMPORDER_LIFETIME = 60 * 60 * 5


def CreateTempOrder(username, tempOrder):
    """
    用于存储临时订单的信息
    """
    if len(tempOrder) == 0:
        return False
    tempOrderKey = "TempOrder:" + username
    if Redis.Exists(tempOrderKey) is True:
        Redis.Delete(tempOrderKey)
    Redis.Sadd(tempOrderKey, *tempOrder)
    return True


def GetTempOrder(username):
    """
    返回临时的订单信息[(id1, count1, addtime1),(id2, count2, addtime2)......]
    """
    tempOrderKey = "TempOrder:" + username
    if Redis.Exists(tempOrderKey) is False:
        return []
    items = list(Redis.Smembers(tempOrderKey))
    cartItemCountKey = "CartIC:" + username
    counts = Redis.Hmget(cartItemCountKey, items)
    cartAddTimeKey = "CartAT:" + username
    addTime = Redis.Hmget(cartAddTimeKey, items)
    tempOrder = []
    for i in range(len(items)):
        tempOrder.append((items[i], counts[i], addTime[i]))
    return tempOrder


def IncInventoryStock(inventid, count):
    """
    用来更新redis中的库存数量
    """
    UpdateInventoryInCache(inventid)
    inventoryKey = "InvInfo:" + str(inventid)
    if Redis.Exists(inventoryKey) is False:
        return None
    remain = Redis.Hincrby(inventoryKey, "Stock", count)
    return remain


def CheckInventoryStock(inventid, count):
    UpdateInventoryInCache(inventid)
    inventoryKey = "InvInfo:" + str(inventid)
    if Redis.Exists(inventoryKey) is False:
        return False
    stock = Redis.Hget(inventoryKey, "Stock")
    if int(stock) < int(count):
        return False
    return True


def ChangeStock(items):
    """
    用于生成订单时候，核对数据库的库存
    输入的为一个数组[(id1,count1),(id2,count2),(id3,count3)......]
    需要保证每个产品的number > 0
    如果失败返回False，成功返回True
    """
    successList = []
    Success = True
    # 执行一次预判断，预判断不执行写操作，用来减少写操作失败的情况
    for item in items:
        if CheckInventoryStock(item[0], item[1]) is False:
            return False
    # 对redis中的库存数进行写操作，如果写操作出现<0的情况，那么进行回滚
    for item in items:
        remain = IncInventoryStock(item[0], - int(item[1]))
        if remain != None:
            successList.append((item[0], int(item[1])))
        if (remain == None) or (remain < 0):
            # 向日志中打印，方便统计实验
            print "Dirty Write in CheckStock: remain = " + str(remain)
            Success = False
            break
    if Success == False:
        # 执行回滚操作
        for item in successList:
            IncInventoryStock(item[0], item[1])
        return False
    else:
        return True

# TODO   并没有加入订单的其它信息，


def CreateUnpayedOrder(username, items):
    """
    生成一个未完成支付的订单
    """
    # 产生Order内容
    Order = {}
    for item in items:
        Order[item[0]] = item[1]
    # 生成新unpaiedOrderId
    unpaiedOrderId = ''.join(str(uuid.uuid1()).split('-'))
    # 加入order清单的购物内容
    unpaiedOrderItemsKey = "UnpaiedOrderItems:" + unpaiedOrderId
    Redis.Hmset(unpaiedOrderItemsKey, Order)
    # 加入到用户的order列表中
    userUnpaiedOrderListKey = "UnpaiedOrderList:" + username
    Redis.Lpush(userUnpaiedOrderListKey, unpaiedOrderId)
    # 删除临时的order
    tempOrderKey = "TempOrder:" + username
    Redis.Delete(tempOrderKey)
    # TODO 将零时的Oder加入到清理列表，可以实现倒计时付款的功能
    # 清理要靠守护进程来实现
    return True

"""
数据库表的缓存操作
"""
#from eweb.models import Product
PROD_INFO_LIFETIME = 60 * 60 * 5


def UpdateProductInCache(productid):
    """
    用于在redis中缓存Product表
    缓存Key和数据库的对应关系：
    ProdInfo:pid{
        "ProdTypeId":producttype,   #类型ID
        "BrandID":brand,            #品牌ID
        "Name":name,                #商品名称
        "Weight":weight,            #重量
        "Package":package_list      #商品内的物品清单
        "New":is_new,               #新品
        "Hot":is_hot,               #热销
        "Commend":is_commend,       #推荐
        "DescImage":description,    #商品描述图片
        "Features":features,        #商品的参数集
        "Colors":colors,            #商品的颜色集
        "Sizes":sizes,              #商品的尺寸集
        "CreateTime":create_time,   #创建时间
    }
    """
    prodInfoKey = "ProdInfo:" + str(productid)
    if Redis.Expire(prodInfoKey, PROD_INFO_LIFETIME) is True:
        return True
    # 不存在
    try:
        product = Product.objects.get(product_id=productid)
    except Exception, e:
        print e
        return False

    ret = Redis.Hmset(prodInfoKey, {
        "ProdTypeId": product.producttype.product_type_id,  # 类型ID
        "BrandID": product.brand.brand_id,  # 品牌ID
        "Name": product.name,  # 商品名称
        "Weight": product.weight,  # 重量
        "Package": product.package_list,  # 商品内的物品清单
        "New": product.is_new,  # 新品
        "Hot": product.is_hot,  # 热销
        "Commend": product.is_commend,  # 推荐
        "DescImage": product.description,  # 商品描述图片
        "Features": product.features.product_feature_id,  # 商品的参数集
        "Colors": product.colors,  # 商品的颜色集
        "Sizes": product.sizes,  # 商品的尺寸集
        "CreateTime": product.create_time,  # 创建时间
    })

    if ret == False:
        print "Redis Hmset product error"
        return False
    Redis.Expire(prodInfoKey, PROD_INFO_LIFETIME)
    # 刷新商品的库存集合
    __UpdateProductInventorySetInCache(product)

    return True


def GetProductInfo(productid, *keys):
    """
    获得产品库中的信息
    返回字典
    """
    result_dict = {}
    prodInfoKey = "ProdInfo:" + str(productid)
    if Redis.Exists(prodInfoKey) is False:
        if UpdateProductInCache(productid) is False:
            print "update " + prodInfoKey + " error"
            return {}
    values = Redis.Hmget(prodInfoKey, *keys)
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict


#from eweb.models import Brand
BRAND_INFO_LIFETIME = 60 * 60 * 24


def UpdateBrandInfoInCache(brandid):
    """
    缓存品牌表
    BrandInfo:BrandID{
        "Name":name,           #品牌名称
        "Desc":description,         #品牌描述
        "LogoUrl":img_url,          #商标图片路径
        "Display":is_display,       #是否会显示在筛选选项中
    }
    """
    brandInfoKey = "BrandInfo:" + brandid
    if Redis.Expire(brandInfoKey, BRAND_INFO_LIFETIME) is True:
        return True

    try:
        brand = Brand.objects.get(brand_id=brandid)
    except Exception, e:
        print e
        return False

    ret = Redis.Hmset(brandInfoKey, {
        "Name": brand.name,  # 品牌名称
        "Desc": brand.description,  # 品牌描述
        "LogoUrl": brand.img_url,  # 商标图片路径
        "Display": int(brand.is_display),  # 是否会显示在筛选选项中
    })

    if ret == False:
        print "Redis Hmset BrandInfo error"
        return False
    Redis.Expire(brandInfoKey, BRAND_INFO_LIFETIME)

    return True


def GetBrandInfo(brandid, *keys):
    """
    获得品牌的信息
    返回字典
    """
    result_dict = {}
    brandInfoKey = "BrandInfo:" + brandid
    if Redis.Exists(brandInfoKey) is False:
        if UpdateBrandInfoInCache(brandid) is False:
            print "update " + brandInfoKey + " error"
            return {}
    values = Redis.Hmget(brandInfoKey, *keys)
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict

ALL_BRANDID_LIFETIME = 60


def UpdateAllBrandIDInCache():
    """

    """
    allBrandIDKey = "AllBrand:ID"
    if Redis.Exists(allBrandIDKey) is True:
        return True
    try:
        brandIDList = Brand.objects.filter(
            is_display=1).values_list('brand_id', flat=True)
    except Exception, e:
        print e
        return False

    if len(brandIDList) == 0:
        return True
    ret = Redis.Sadd(allBrandIDKey, *brandIDList)
    if ret == False:
        print "Redis Sadd  AllBrandID error"
        return False
    Redis.Expire(allBrandIDKey, ALL_BRANDID_LIFETIME)
    return True


def GetAllBrandID():
    """
    获得所有的品牌
    返回一个品牌ID的集合
    """
    allBrandIDKey = "AllBrand:ID"
    if Redis.Exists(allBrandIDKey) is False:
        if UpdateAllBrandIDInCache() is False:
            print "update " + allBrandIDKey + " error"
            return []
    values = Redis.Smembers(allBrandIDKey)
    result_list = list(values)
    return result_list


def GetAllBrandName():
    """
    获得所有品牌ID和品牌名的字典集
    返回一个字典
    {ID1:name1, ID2:name2, ID3:name3,.....}
    """
    IDList = GetAllBrandID()
    result_dict = {}
    for brandid in IDList:
        result_dict[brandid] = GetBrandInfo(brandid, "Name").get("Name")
    return result_dict

#from eweb.models import Producttype
PRODUCTTYPE_INFO_LIFETIME = 60 * 60 * 24


def UpdateProductTypeInfoInCache(prodtypeid):
    """
    缓存商品类型表
    ProdTypeInfo:ProdTypeId{
        "Name":name,                #类型名称
        "FatherTypeId":parent_id,   #父商品类型ID
        "Note":note,                #备注(用于搜索页面商品描述)
        "Display":is_display,       #是否在搜索时可见
    }
    """
    prodtypeInfoKey = "ProdTypeInfo:" + str(prodtypeid)
    if Redis.Expire(prodtypeInfoKey, PRODUCTTYPE_INFO_LIFETIME) is True:
        return True

    try:
        prodtype = Producttype.objects.get(product_type_id=prodtypeid)
    except Exception, e:
        print e
        return False

    ret = Redis.Hmset(prodtypeInfoKey, {
        "Name": prodtype.name,  # 类型名称
        "FatherTypeId": prodtype.parent_id,  # 父商品类型ID
        "Note": prodtype.note,  # 备注(用于搜索页面商品描述)
        "Display": int(prodtype.is_display),  # 是否在搜索时可见
    })

    if ret == False:
        print "Redis Hmset prodtype error"
        return False
    Redis.Expire(prodtypeInfoKey, PRODUCTTYPE_INFO_LIFETIME)
    return True


def GetProductTypeInfo(prodtypeid, *keys):
    """
    获得产品类型的信息
    返回字典
    """
    result_dict = {}
    prodtypeInfoKey = "ProdTypeInfo:" + str(prodtypeid)
    if Redis.Exists(prodtypeInfoKey) is False:
        if UpdateProductTypeInfoInCache(prodtypeid) is False:
            print "update " + prodtypeInfoKey + " error"
            return {}
    values = Redis.Hmget(prodtypeInfoKey, *keys)
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict

ALL_PRODTYPEID_LIFETIME = 60


def UpdateAllProdTypeIDInCache():
    """

    """
    allProdTypeIDKey = "AllProdType:ID"
    if Redis.Exists(allProdTypeIDKey) is True:
        return True
    try:
        allProdIDList = Producttype.objects.filter(
            is_display=1).values_list('product_type_id', flat=True)
    except Exception, e:
        print e
        return False

    if len(allProdIDList) == 0:
        return True
    ret = Redis.Sadd(allProdTypeIDKey, *allProdIDList)
    if ret == False:
        print "Redis Sadd  allProdTypeID error"
        return False
    Redis.Expire(allProdTypeIDKey, ALL_PRODTYPEID_LIFETIME)
    return True


def GetAllProdTypeID():
    """
    获得所有的产品类型ID
    返回一个产品类型ID的集合
    """
    allProductTypeIDKey = "AllProdType:ID"
    if Redis.Exists(allProductTypeIDKey) is False:
        if UpdateAllProdTypeIDInCache() is False:
            print "update " + allProductTypeIDKey + " error"
            return []
    values = Redis.Smembers(allProductTypeIDKey)
    result_list = list(values)
    return result_list


def GetAllProdTypeName():
    """
    获得所有类型ID和类型名的字典集
    返回一个字典
    {ID1:name1, ID2:name2, ID3:name3,.....}
    """
    IDList = GetAllProdTypeID()
    result_dict = {}
    for prodtypeid in IDList:
        result_dict[prodtypeid] = GetProductTypeInfo(
            prodtypeid, "Name").get("Name")
    return result_dict

#from eweb.models import Productfeature
FEATURE_INFO_LIFETIME = 60 * 60 * 24


def UpdateFeatureInfoInCache(featureid):
    """
    缓存商品属性表
    FeatureInfo:FeatureId{
        "Name":name,                #类型名称
        "Del":is_del,       #是否已经废弃
    }
    """

    featureInfoKey = "FeatureInfo:" + str(featureid)
    if Redis.Expire(featureInfoKey, FEATURE_INFO_LIFETIME) is True:
        return True

    try:
        feature = Productfeature.objects.get(product_feature_id=featureid)
    except Exception, e:
        print e
        return False

    ret = Redis.Hmset(featureInfoKey, {
        "Name": feature.name,  # 类型名称
        "Del": int(feature.is_del),  # 是否在搜索时可见
    })

    if ret == False:
        print "Redis Hmset feature error"
        return False
    Redis.Expire(featureInfoKey, FEATURE_INFO_LIFETIME)
    return True


def GetFeatureInfo(featureid, *keys):
    """
    获得产品属性的信息
    返回字典
    """
    result_dict = {}
    featureInfoKey = "FeatureInfo:" + str(featureid)
    if Redis.Exists(featureInfoKey) is False:
        if UpdateFeatureInfoInCache(featureid) is False:
            print "update " + featureInfoKey + " error"
            return {}
    values = Redis.Hmget(featureInfoKey, *keys)
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict

ALL_PRODFEATUREID_LIFETIME = 60


def UpdateAllFeatureIDInCache():
    """

    """
    allFeatureIDKey = "AllFeature:ID"
    if Redis.Exists(allFeatureIDKey) is True:
        return True
    try:
        allFeatureIDList = Productfeature.objects.filter(
            is_del=0).values_list('product_feature_id', flat=True)
    except Exception, e:
        print e
        return False

    if len(allFeatureIDList) == 0:
        return True
    ret = Redis.Sadd(allFeatureIDKey, *allFeatureIDList)
    if ret == False:
        print "Redis Sadd  allFeatureID error"
        return False
    Redis.Expire(allFeatureIDKey, ALL_PRODFEATUREID_LIFETIME)
    return True


def GetAllFeatureID():
    """
    获得所有的属性ID
    返回一个产品属性ID的集合
    """
    allFeatureIDKey = "AllFeature:ID"
    if Redis.Exists(allFeatureIDKey) is False:
        if UpdateAllFeatureIDInCache() is False:
            print "update " + allFeatureIDKey + " error"
            return []
    values = Redis.Smembers(allFeatureIDKey)
    result_list = list(values)
    return result_list


def GetAllFeatureName():
    """
    获得所有属性ID和属性名的字典集
    返回一个字典
    {ID1:name1, ID2:name2, ID3:name3,.....}
    """
    IDList = GetAllFeatureID()
    result_dict = {}
    for featureid in IDList:
        result_dict[featureid] = GetFeatureInfo(featureid, "Name").get("Name")
    return result_dict

#from eweb.models import Img
PROD_IMGS_LIFETIME = 60 * 60 * 5


def UpdateProductImageSetInCache(productid):
    """
    用于记录一个商品的图片集
    ProdImgSet:pid[]
    """
    try:
        product = Product.objects.get(product_id=productid)
    except Exception, e:
        print e
        return False
    return __UpdateProductImageSetInCache(product, productid)


def __UpdateProductImageSetInCache(product, productid=None):
    """
    内部实现
    """
    if productid == None:
        productid = str(product.product_id)

    prodImgSetKey = "ProdImgSet:" + str(productid)
    if Redis.Expire(prodImgSetKey, PROD_IMGS_LIFETIME) is True:
        return True

    imgList = Img.objects.filter(product=product).values_list('url', flat=True)
    if len(imgList) == 0:
        return True
    ret = Redis.Sadd(prodImgSetKey, *imgList)
    if ret == False:
        print "Redis Sadd  prodInvSet error"
        return False
    Redis.Expire(prodImgSetKey, PROD_IMGS_LIFETIME)
    return True


def GetProductImage(productid):
    """
    获得一个商品的所有图片
    返回list
    """
    prodImgSetKey = "ProdImgSet:" + str(productid)
    if Redis.Exists(prodImgSetKey) is False:
        if UpdateProductImageSetInCache(productid) is False:
            print "update " + prodImgSetKey + " error"
            return {}
    values = Redis.Smembers(prodImgSetKey)
    result_list = list(values)
    return result_list


#from eweb.models import Sku
PROD_INVENT_LIFETIME = 60 * 60 * 5


def UpdateProductInventorySetInCache(productid):
    """
    用于记录一个商品的库存
    ProdInvSet:pid[]
    """
    try:
        product = Product.objects.get(product_id=productid)
    except Exception, e:
        print e
        return False

    return __UpdateProductInventorySetInCache(product, productid)


def __UpdateProductInventorySetInCache(product, productid=None):
    """
    内部实现
    """
    if productid == None:
        productid = str(product.product_id)

    prodInvSetKey = "ProdInvSet:" + str(productid)
    if Redis.Expire(prodInvSetKey, PROD_INVENT_LIFETIME) is True:
        return True

    inventList = Sku.objects.filter(
        product=product).values_list('sku_id', flat=True)
    if len(inventList) == 0:
        return True
    ret = Redis.Sadd(prodInvSetKey, *inventList)
    if ret == False:
        print "Redis Sadd  ProdInvSet error"
        return False
    Redis.Expire(prodInvSetKey, PROD_INVENT_LIFETIME)
    return True


def GetProductInventory(productid):
    """
    获得一个商品的所有库存列表
    返回list
    """
    prodInvSetKey = "ProdInvSet:" + str(productid)
    if Redis.Exists(prodInvSetKey) is False:
        if UpdateProductInventorySetInCache(productid) is False:
            print "update " + prodInvSetKey + " error"
            return []
    values = Redis.Smembers(prodInvSetKey)
    result_list = list(values)
    return result_list

#from eweb.models import Sku
INVENTORY_LIFETIME = 60 * 60 * 5


def UpdateInventoryInCache(inventoryid):
    """
    用于在redis中缓存库存信息
    缓存Key和数据库的对应关系：
    InvInfo:inventoryid{
        "ProdectID":product.product_id,     #商品ID
        "Color":color.color,          #颜色ID
        "Size":sizes,               #尺码
        "DeliveFee":delive_fee,     #运费
        "Price":price,              #售价
        "Stock":stock,              #销量
        "Location":location,        #货架号
        "InvImg":sku_img,           #库存照片
        "InvStatus":sku_status,     #是历史库存还是新品
        "InvType":sku_type,         #是赠品还是普通
        "Sales":sales,              #历史销量
    }
    """
    inventoryKey = "InvInfo:" + str(inventoryid)
    if Redis.Expire(inventoryKey, INVENTORY_LIFETIME) is True:
        return True

    try:
        inventory = Sku.objects.get(sku_id=inventoryid)
    except Exception, e:
        print e
        return False

    ret = Redis.Hmset(inventoryKey, {
        "ProdectID": inventory.product.product_id,  # 商品ID
        "Color": inventory.color.color,  # 颜色ID
        "Size": inventory.sizes,  # 尺码
        "DeliveFee": inventory.delive_fee,  # 运费
        "Price": inventory.price,  # 售价
        "Stock": inventory.stock,  # 库存量
        "Location": inventory.location,  # 货架号
        "InvImg": inventory.sku_img,  # 库存照片
        "InvStatus": inventory.sku_status,  # 是历史库存还是新品
        "InvType": inventory.sku_type,  # 是赠品还是普通
        "Sales": inventory.sales,  # 历史销量
    })

    if ret == False:
        print "Redis Hmset inventory error"
        return False
    Redis.Expire(inventoryKey, INVENTORY_LIFETIME)
    return True


def GetInventorInfo(inventid, *keys):
    """
    获得库存的信息
    返回字典
    """
    result_dict = {}
    inventoryKey = "InvInfo:" + str(inventid)
    if Redis.Exists(inventoryKey) is False:
        if UpdateInventoryInCache(inventid) is False:
            print "update " + inventoryKey + " error"
            return {}
    values = Redis.Hmget(inventoryKey, *keys)
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict

#from eweb.models import Buyer
USER_INFO_LIFETIME = 60 * 60 * 3


def UpdateUserInCache(user):
    """
    在redis中缓存用户信息
    缓存Key和数据库的对应关系：
    UserInfo:username{
        "Email":user.email,
        "Gender":gender,
        "RegTime":register_time,
        "RealName":real_name,
        "Province":province,
        "City":city,
        "Town":town,
        "Addr":addr,
        "CssID",     #废弃               #CSessionID在创建会话的时候更新
    } expire USER_INFO_LIFETIME
    """
    username = user.get_username()
    if username == None:
        print "Not Find A UserName"
        return False

    userinfoKey = "UserInfo:" + username
    if Redis.Expire(userinfoKey, USER_INFO_LIFETIME) is True:
        return True

    try:
        userinfo = Buyer.objects.get(user=user)
    except Exception, e:
        print e
        return False

    ret = Redis.Hmset(userinfoKey, {
        "Email": userinfo.user.email,
        "Gender": userinfo.gender,
        "RegTime": userinfo.register_time,
        "RealName": userinfo.real_name,
        "Province": userinfo.province,
        "City": userinfo.city,
        "Town": userinfo.town,
        "Addr": userinfo.addr,
    })

    if ret == False:
        print "Redis Hmset userinfo error"
        return False

    Redis.Expire(userinfoKey, USER_INFO_LIFETIME)
    return True


def GetUserInfo(user, *keys):
    """
    获得用户的信息
    返回字典
    """
    username = user.get_username()
    if username == None:
        print "Not Find A UserName"
        return False

    result_dict = {}
    userinfoKey = "UserInfo:" + username
    if Redis.Exists(userinfoKey) is False:
        if UpdateInventoryInCache(user) is False:
            print "update " + userinfoKey + " error"
            return {}
    values = Redis.Hmget(userinfoKey, *keys)
    for i in range(len(keys)):
        result_dict[keys[i]] = values[i]
    return result_dict

"""
清空缓存中的数据，给后台管理提供的接口
"""
# TODO


def DeleteProductFromCache(*productids):
    prodInfoKeys = []
    for productid in productids:
        prodInfoKeys.append("ProdInfo:" + str(productid))
    Redis.Delete(*prodInfoKeys)
    return True
