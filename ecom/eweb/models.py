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
    user = models.OneToOneField(User,verbose_name="用户名")
    gender = models.CharField(
        u'性别', choices=TITLE_CHOICES, max_length=10, null=True, blank=True)
    register_time = models.DateTimeField(auto_now_add=True,verbose_name='注册时间')
    real_name = models.CharField(max_length=20, blank=True,verbose_name='真实姓名')
    province = models.CharField(max_length=20, blank=True,verbose_name='省')
    city = models.CharField(max_length=20, blank=True,verbose_name='市')
    town = models.CharField(max_length=20, blank=True,verbose_name='县')
    addr = models.CharField(max_length=80, blank=True,verbose_name='地址')

    def __unicode__(self):
        return self.user.username

class Brand(models.Model):
    '''
    商品品牌
    名称,描述,图片Url(存在static目录下),是否可见'1:可见 0:不可见'
    '''
    name = models.CharField(max_length=20,verbose_name='商品名称')
    description = models.CharField(max_length=80,verbose_name='描述')
    img_url = models.CharField(max_length=80,verbose_name='图片url')
    is_display = models.BooleanField(default=True,verbose_name='是否可见')

    def __unicode__(self):
        return self.name


class Producttype(models.Model):
    '''
    商品类型
    名称,父商品类型id,备注(用于搜索页面商品描述),是否可见 1:可见 0:不可见
    '''
    name = models.CharField(max_length=20,verbose_name='用户名')
    parent_id = models.IntegerField(verbose_name='父商品类型id')
    note = models.CharField(max_length=50,verbose_name='备注')
    is_display = models.BooleanField(default=True,verbose_name='是否可见')

    def __unicode__(self):
        return self.name


class Productfeature(models.Model):
    '''
    商品属性
    名称,是否废弃:1:未废弃,0:废弃了
    '''
    name = models.CharField(max_length=20,verbose_name='商品属性')
    is_del = models.BooleanField(default=True,verbose_name='是否废弃')

    def __unicode__(self):
        return self.name


class Product(models.Model):
    '''
    商品表 (显示商品详情页面)
    ID或商品编号(全国唯一),类型ID,品牌ID,商品名称,重量(单位:克),是否新品(0旧品,1新品),
    是否热销(0,否 1:是),推荐(1推荐 0 不推荐),上下架(0否 1是),是否删除(0删除,1没删除),销量,商品描述(需要图片描述的路径),
    包装清单,商品属性集,颜色集,尺寸集,添加时间
    '''
    pid = models.IntegerField(primary_key=True,verbose_name='ID或商品编号')
    type_id = models.ForeignKey(Producttype,verbose_name='类型ID')
    brand_id = models.ForeignKey(Brand,verbose_name='品牌ID')
    name = models.CharField(max_length=50,verbose_name='商品名称')
    weight = models.FloatField(verbose_name='重量（克）')
    is_new = models.BooleanField(default=True,verbose_name='是否新品')
    is_hot = models.BooleanField(default=True,verbose_name='是否热销')
    is_commend = models.BooleanField(default=False,verbose_name='推荐')
    is_show = models.BooleanField(default=False,verbose_name='上下架')
    is_del = models.BooleanField(default=True,verbose_name='是否删除')
    description = models.ImageField(upload_to='productimages', blank=False,verbose_name='商品描述')
    package_list = models.CharField(max_length=100,verbose_name='包装清单')

    features = models.CharField(max_length=100,verbose_name='商品属性集')
    colors = models.CharField(max_length=100,verbose_name='颜色集')
    sizes = models.CharField(max_length=100,verbose_name='尺寸集')

    create_time = models.DateTimeField(verbose_name='添加时间')

    def __unicode__(self):
        return self.name


class Img(models.Model):
    '''
    商品图片
    商品ID,图片url
    是否默认 0否 1是
    '''
    product_id = models.ForeignKey(Product,verbose_name='商品ID')
    url = models.ImageField(upload_to='productimages', blank=False,verbose_name='图片Url')
    is_def = models.BooleanField(default=False,verbose_name='是否默认')

    def __unicode__(self):
        return self.product_id.name


class Color(models.Model):
    '''
    商品颜色
    颜色,颜色父ID
    '''
    color = models.CharField(max_length=20,verbose_name='商品颜色')
    parent_id = models.IntegerField(verbose_name='颜色父ID')

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
    product_id = models.ForeignKey(Product,verbose_name='商品ID')
    color_id = models.ForeignKey(Color,verbose_name='颜色ID')
    sizes = models.CharField(max_length=5,verbose_name='尺码')
    delive_fee = models.IntegerField(default=10,verbose_name='运费')
    price = models.FloatField(verbose_name='售价')
    stock = models.IntegerField(verbose_name='库存')
    location = models.CharField(max_length=50,verbose_name='仓库位置:货架号')

    sku_img = models.ImageField(upload_to='productimages',verbose_name='SKU图片')

    sku_status = models.BooleanField(default=False)
    sku_type = models.BooleanField(default=True)
    sales = models.IntegerField(verbose_name='销量')

    def __unicode__(self):
        return self.product_id.name


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
    order_id = models.IntegerField(primary_key=True,verbose_name='订单ID')
    deliver_fee = models.IntegerField(verbose_name='运费')
    total_fee = models.FloatField(verbose_name='应付金额')
    order_price = models.FloatField(verbose_name='订单金额')
    payment_way = models.CharField(max_length=10,verbose_name='支付方式')
    payment_cash = models.CharField(max_length=10,verbose_name='货到付款方式')
    delivery = models.DateField(auto_now_add=True,verbose_name='送货时间')
    is_confirm = models.CharField(max_length=10,verbose_name='是否电话确认')
    is_pay = models.CharField(max_length=10,verbose_name='支付状态')
    order_state = models.CharField(max_length=10,verbose_name='订单状态')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='订单生成时间')
    note = models.CharField(max_length=100,verbose_name='附言')
    buyer_id = models.ForeignKey(Buyer,verbose_name='用户名')

    def __unicode__(self):
        return self.buyer_id.user.username


class Orderdetail(models.Model):
    '''
    订单详情表(具体的订单参数)，购物车需要
    订单ID,商品编号,商品名称,颜色名称,尺码,商品销售价,购买数量
    '''
    order_id = models.ForeignKey(Order,verbose_name='订单ID')
    product_id = models.IntegerField(verbose_name='商品编号')
    product_name = models.CharField(max_length=80,verbose_name='商品名称')
    color = models.CharField(max_length=5,verbose_name='颜色名称')
    size = models.CharField(max_length=5,verbose_name='尺码')
    price = models.FloatField(verbose_name='商品销售价')
    amount = models.IntegerField(default=1,verbose_name='购买数量')

    def __unicode__(self):
        return self.product_name
