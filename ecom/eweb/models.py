# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
TITLE_CHOICES = (('0', '保密'),
                 ('1', '男'),
                 ('2', '女'),)


class Buyer(models.Model):
    '''
    商城购买者
    用户,性别,注册时间,真实名字,省ID,市ID,县ID,地址,
    '''
    user = models.OneToOneField(User)
    gender = models.CharField(
        u'性别', choices=TITLE_CHOICES, max_length=10, null=True, blank=True)
    register_time = models.DateTimeField(auto_now_add=True,)
    real_name = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    town = models.CharField(max_length=20, blank=True)
    addr = models.CharField(max_length=80, blank=True)

    def __unicode__(self):
        return self.user.username


class Brand(models.Model):
    '''
    商品品牌
    名称,描述,图片Url(存在static目录下),是否可见'1:可见 0:不可见'
    '''
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=80)
    img_url = models.CharField(max_length=80)
    is_display = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Producttype(models.Model):
    '''
    商品类型
    名称,父商品类型id,备注(用于搜索页面商品描述),是否可见 1:可见 0:不可见
    '''
    name = models.CharField(max_length=20)
    parent_id = models.IntegerField()
    note = models.CharField(max_length=50)
    is_display = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Productfeature(models.Model):
    '''
    商品属性
    名称,是否废弃:1:未废弃,0:废弃了
    '''
    name = models.CharField(max_length=20)
    is_del = models.BooleanField(default=True)

    def __unicode__(self):
        return self.pname


class Product(models.Model):
    '''
    商品表 (显示商品详情页面)
    ID或商品编号(全国唯一),类型ID,品牌ID,商品名称,重量(单位:克),是否新品(0旧品,1新品),
    是否热销(0,否 1:是),推荐(1推荐 0 不推荐),上下架(0否 1是),是否删除(0删除,1没删除),销量,商品描述(需要图片描述的路径),
    包装清单,商品属性集,颜色集,尺寸集,添加时间
    '''
    pid = models.IntegerField(primary_key=True)
    type_id = models.ForeignKey(Producttype)
    brand_id = models.ForeignKey(Brand)
    name = models.CharField(max_length=50)
    weight = models.FloatField(max_digits=5, decimal_places=2)
    is_new = models.BooleanField(default=True)
    is_hot = models.BooleanField(default=True)
    is_commend = models.BooleanField(default=False)
    is_show = models.BooleanField(default=False)
    is_del = models.BooleanField(default=True)
    description = models.ImageField(upload_to='productimages', blank=False)
    package_list = models.CharField(max_length=100)

    features = models.CharField(max_length=100)
    colors = models.CharField(max_length=100)
    sizes = models.CharField(max_length=100)

    create_time = models.DateTimeField()

    def __unicode__(self):
        return self.name


class Img(models.Model):
    '''
    商品图片
    商品ID,图片url
    是否默认 0否 1是
    '''
    product_id = models.ForeignKey(Product)
    url = models.ImageField(upload_to='productimages', blank=False)
    is_def = models.BooleanField(default=False)

    def __unicode__(self):
        return self.product_id.name


class Color(models.Model):
    '''
    商品颜色
    颜色,颜色父ID
    '''
    color = models.CharField(max_length=20)
    parent_id = models.IntegerField()

    def __unicode__(self):
        return self.color


class Sku(models.Model):
    '''
    库存(最小销售单元)
    商品ID,颜色ID,尺码,运费 默认10元,售价,库存,仓库位置:货架号,SKU图片,
    0,历史 1最新
    0:赠品,1普通
    销量
    '''
    product_id = models.ForeignKey(Product)
    color_id = models.ForeignKey(Color)
    sizes = models.CharField(max_length=5)
    delive_fee = models.IntegerField(default=10)
    price = models.FloatField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    location = models.CharField(max_length=50)

    sku_img = models.ImageField(upload_to='productimages')

    sku_status = models.BooleanField(default=False)
    sku_type = models.BooleanField(default=True)
    sales = models.IntegerField()

    def __unicode__(self):
        return self.product_id.name


class Orderdetail(models.Model):
    '''
    订单详情表(具体的订单参数)，购物车需要
    订单ID,商品编号,商品名称,颜色名称,尺码,商品销售价,购买数量
    '''
    order_id = models.ForeignKey(Order)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=80)
    color = models.CharField(max_length=5)
    size = models.CharField(max_length=5)
    price = models.FloatField(max_digits=5, decimal_places=2)
    amount = models.IntegerField(default=1)

    def __unicode__(self):
        return self.product_name


class Order(models.Model):
    '''
    订单表
    '运费',
    '应付金额',
    '订单金额',
    '支付方式 0:到付 1:在线 2:邮局 3:公司转帐',
    '货到付款方式.0现金,1POS刷卡',
    '送货时间',
    '是否电话确认 1:是  0: 否',
    '支付状态 :0到付1待付款,2已付款,3待退款,4退款成功,5退款失败',
    订单状态 0:提交订单 1:仓库配货 2:商品出库 3:等待收货 4:完成 5待退货 6已退货',
    '订单生成时间',
    '附言',
    '用户名',
    '''
    order_id = models.IntegerField(primary_key=True)
    deliver_fee = models.IntegerField()
    total_fee = models.FloatField(max_digits=5, decimal_places=2)
    order_price = models.FloatField(max_digits=5, decimal_places=2)
    payment_way = models.CharField(max_length=10)
    payment_cash = models.CharField(max_length=10)
    delivery = models.DateField(auto_now_add=True)
    is_confirm = models.CharField(max_length=10)
    is_pay = models.CharField(max_length=10)
    order_state = models.CharField(max_length=10)
    create_date = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=100)
    buyer_id = models.ForeignKey(Buyer)

    def __unicode__(self):
        return self.buyer_id.user.username
