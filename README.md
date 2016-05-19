PK
    eq�H�A(��0  �0   $ 电商项目技术文档.mdup  ��Wa电商项目技术文档.md#电商项目技术文档
[TOC]
##运行环境：
软件环境：
Centos6.5

硬件环境：
ubuntu14.04

开发工具：
MySQL+Redis+Django+Sublime+FastDFS+Nginx+uWSGI

##项目描述：


##Redis缓存模块：

###用的Redis的地方
1.缓存对商品内容进行缓存
2.分布式集群架构中的session分离，解决session异步问题
3.任务队列（秒杀，抢购等等）
4.数据过期处理（将缓存中过期的商品数据进行处理，可以精确到毫秒）
5.购物车数据的保存

###具体步骤
一、对redis接口进行封装(我们自己封装的接口都放在项目的databaselib目录下)
```python
#部分内容如下
ConnectionPool = redis.ConnectionPool.from_url('redis://127.0.0.1:6379/0')


class RedisBase:
    """
    封装redis的接口
    """
    def __init__ (self):
        self._redis = redis.Redis(connection_pool = ConnectionPool)
        return

    def Append(self, key, value):
        ret = self._redis.append(key, value)
        return ret

    def Delete(self, *names):
        ret = self._redis.delete(*names)
        return ret
```
二、使用redis接口进行数据库内容进行设置，`包含了对数据库的Server层的操作
封装应用层了对数据库的所有业务上的操作通过db_base.py的接口实现，放在databaselib中的db_server.py中。`


对于如何用redis架构秒杀系统，这个网站有提及
[http://itindex.net/detail/55445-redis-秒杀-系统]值得学习一下

###Redis缓存分三类：
永久缓存：用户购物车信息

暂时缓存的：用户的session

定时缓存的：从数据库中取出的部分



##主页技术
###功能模块
1.推荐商品， 
2.热销商品， 
3.满足筛选条件的商品（ 默认下是随机从数据库选取的）
4.条件筛选

###相关技术
juery， ajax 局部刷新
###具体步骤
1.推荐商品：
（ 1） 根据是否热销从数据库中取出前四件商品：
关于如何从数据库取数据参考 django 文档中的查询。
`hot_list1=Product.objects.filter(is_hot=True)[0:4]`
（ 2） 找出每件商品的名称， 图片， 价格
```python
for one in hot_list1:
hot_List = {}
hot_List['id'] = one.product_id
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
```
2.热销商品：（ 方法同上）
```python
commend_list1 = Product.objects.filter(is_commend=True)[0:4]
for one in commend_list1:
commend_List = {}
commend_List['id'] = one.product_id
commend_List['name'] = one.name
img_temp = Img.objects.filter(product=one)
for a in img_temp:
commend_List['img'] = str(a.url)
sku_temp = Sku.objects.filter(product=one)
for one1 in sku_temp:
commend_List['price'] = one1.price
commend_list.append(commend_List)
```
3.条件过滤
（ 1） 在 js 文件夹下新建一个.js 文件， 并在 homepage 的 <head>之间引入该 js 文件
（ 2） 在 js 文件中写相关的代码， 该部分主要用到的技术是 jquery， 通过 html 中的 class 和 id来找到相应的 html 代码，并对该部分进行修改和增加，其中需要了解是 html 知识， css、javaScript和 jquery 函数的写法。

以下是实现当点击选择品牌的某一选项时， 会将该选项显示在“显示条件” 中， 并且任何时刻只能显示一个品牌。 例如： 若选择了 SIBOON,那么再点击沙落尔品牌时， SIBOON 则会被沙洛尔替换。
```javascript
$(document).ready(function() {
$(".select1 li").click(function() {
$(this).addClass("selected").siblings().removeClass("selected");
if ($(this).hasClass("select-all")) {
$("#selectA").remove();
} else {
var copyThisA = $(this).clone();
if ($("#selectA").length > 0) {
$("#selectA a").html($(this).text());
} else {
$(".alert-sm b").append(copyThisA.attr("id", "selectA"));
}
}
});
$(document).ready(function() {
$(".select1 li").click(function() {
$(this).addClass("selected").siblings().removeClass("selected");
if ($(this).hasClass("select-all")) {
$("#selectA").remove();
} else {
var copyThisA = $(this).clone();
if ($("#selectA").length > 0) {
$("#selectA a").html($(this).text());
} else {
$(".alert-sm b").append(copyThisA.attr("id", "selectA"));
}
}
});
});
```
同理， 则材质和类别实现的方法同上。
（ 3） 除了将选择的条件显示在“ 显示条件” 中以外， 还需要将选择的条件传给后台， 后台再根据条件从数据库中筛选符合条件的 商品， 并在主页中显示。 新建一个 filter-ajax.js 文件。
在 filter-ajax.js 中，
```javascript
(".selected-1 a").click(function() {
var a = $(this).text()+'1'
$.getJSON('showproduct', {'a':a}, function(ret){
$('#product-list').html('');
$.each(ret, function(homepage,item){
$('#product-list').append('<li><a href=""><img
class="center-block"src="/res/'+item['img']+'"></a><div class="summary"><a
href="">'+item['name']+'</a></div><div class="price"><b>售价:'+item['price']+'</b></div><div
class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button
type="button" class="btn btn-default btn-xs">加入购物车</button></li>')
})
});
})
```
以上是当点击品牌中的“ all” 时，会将“ all1” 这个字符串通过变量 a 传给前台， 这里加上一个“ 1” 是为了区别下面的“ all”， `$.getJSON('showproduct', {'a':a}, function(ret)`这个函数可以 url 到views 中的 showproduct 函数， 并将 a 传过去， 最后将传回来的 json 包进行解析得到 ret。在 views 中， 首先定义了六个全局变量， 前三个全局变量分别是保存鼠标所选择的品牌， 材质和类别的选项， 后三个全局变量分别保存品牌， 材质和类别的所有选项， 利用集合元素的唯一性， 通过对 A_BRAND 与 BRAND_LAST 求交集来保存点击的品牌名称通过 B_BRAND 与FEATURE_LAST 求交集来保存点击的材质名称， 通过对 TYPE_LAST 与 C_BRAND 求交集来保存点击的类别的名称。 第一段代码如下,后两段同理。
```python
global A_BRAND
global B_BRAND
global C_BRAND
global BRAND_LAST
global FEATURE_LAST
global TYPE_LAST
brandname_list1 = GetAllBrandName()
for brand in brandname_list1:
A_BRAND.add(brandname_list1[brand])
feature_list1 = GetAllFeatureName()
for feature in feature_list1:
B_BRAND.add(feature_list1[feature])
type_list1 = GetAllProdTypeName()
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
```
经过上面三段代码 ， BRADN_LAST、 FEATURE_LAST 和 TYPE_LAST 分别保存的是品牌、 材质和类型， 接下来通过 len()来判断是否为空， 然后分八种不同情况从数据库进行筛选（ 此处应该有更好的方法， 但是当时没想出来， 就用了最笨的方法）
下面列举了其中一种情况， 当品牌和材质不为空时， 类型为空时：
```python
elif len(BRAND_LAST) == 1 and len(FEATURE_LAST) == 1 and len(TYPE_LAST) == 0:
for i in BRAND_LAST:
Product_Brand = Brand.objects.filter(name=str(i))
for j in FEATURE_LAST:
Feature_Brand=Productfeature.objects.filter(name=str(j))
for pb in Product_Brand:
for pf in Feature_Brand:
Product_b = Product.objects.filter(brand=pb,features=pf)
for a in Product_b:
Product_dic = {}
Product_dic['id'] = a.product_id
Product_dic['name'] = a.name
temp = Img.objects.filter(product=a)
for a1 in temp:
Product_dic['img'] = str(a1.url)
temp1 = Sku.objects.filter(product=a)
for a2 in temp1:
Product_dic['price'] = a2.price
product_list.append(Product_dic)
```
剩下七种情况同上。
最后将得到的一个产品列表打包成 json 传给后台。
`return HttpResponse(json.dumps(product_list),content_type='application/json')`
回到 filter-ajax.js 文件中。 function(ret)函数， ret 是解析 json 包后的产品的列表，
`$('#product-list').html('')`将 id 为 product-list 的 html 部分清空，
通过`$.each(ret,function(homepage,item)`遍历每一件商品， 并将商品的信息重新显示布局在该 html中。 代码如下：
```javascript
$(".selected-1 a").click(function() {
var a = $(this).text()+'1'
$.getJSON('showproduct', {'a':a}, function(ret){
$('#product-list').html('');
$.each(ret, function(homepage,item){
$('#product-list').append('<li><a href=""><img
class="center-block"src="/res/'+item['img']+'"></a><div class="summary"><a
href="">'+item['name']+'</a></div><div class="price"><b>售价:'+item['price']+'</b></div><div
class="list-show-eva"><i class="icon-main icon-eva-6"></i><a href="">北京有货</a></div><button
type="button" class="btn btn-default btn-xs">加入购物车</button></li>')
})
});
})
```
至此， 当点击第一个“ all” 的情况已经写完， 剩下的三种情况如上（ 两个“ all” 的情况和任意其他选项的情况。）
###参考的技术网站
1.jquery 条件过滤， 仿淘宝
http://www.w3cdown.com/course/81.html
2.Django1.6+jQuery Ajax + JSON 实现页面局部实时刷新
http://www.ziliao1.com/Article/Show/A6EA4BFFCED28B15F02F9A67EBF94EAF.html
3JQuery 的 Ajax 请求实现局部刷新的简单实例
http://www.jb51.net/article/46622.htm
4.ajax 数据库实例
http://www.w3school.com.cn/ajax/ajax_database.asp

##购物车模块
###业务流程：
1.如果没有登入：那么购物信息保存在Cookie中
2.如果已经登入：那么购物信息保存在Redis中
3.如果从没有登入到已经登入：需要将Cookie中的商品取出来，和Redis中的商品进行合并

一、在views.py中，分别处理get,post请求
```python
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
```
然后自己定义了两个函数去单独处理业务逻辑：
```python
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
```
get和post获取的状态将通过JsonResponse返回到js中，购物车相关js代码我们放在cart.js中




##商品详情页
sku联动技术


##其它未完成
###几个集群搭建：
Redis集群
Solr集群
Mycat+Mysql集群
FastDFS集群


###支付系统：


PK 
    eq�H�A(��0  �0   $               电商项目技术文档.mdup  ��Wa电商项目技术文档.mdPK      m   -1    