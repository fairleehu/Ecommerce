#coding = utf-8
from django.contrib import admin
from eweb.models import *



class BrandAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'img_url','is_display')
	search_fields = ('name', 'description', 'img_url','is_display')
	list_filter = ["name",'description','is_display']

class BuyerAdmin(admin.ModelAdmin):
	list_display = ('user', 'gender', 'register_time','real_name', 'province','city', 'town','addr')
	search_fields =('user', 'gender', 'register_time','real_name', 'province','city', 'town','addr')
	list_filter =['user', 'gender', 'register_time','real_name', 'province','city', 'town','addr']

class ColorAdmin(admin.ModelAdmin):
	list_display = ('color', 'parent_id')
	search_fields =('color', 'parent_id')
	list_filter =['color', 'parent_id']

class ImgAdmin(admin.ModelAdmin):
    	list_display = ('product_id', 'url','is_def')
    	search_fields =('product_id','is_def')
    	list_filter =['product_id','is_def']

class ProducttypeAdmin(admin.ModelAdmin):
    	list_display = ('name' ,'parent_id','note','is_display')
    	search_fields = ('name' ,'parent_id','note','is_display')
    	list_filter =['name' ,'parent_id','note','is_display']

class ProductfeatureAdmin(admin.ModelAdmin):
    	list_display = ('name','is_del')
    	search_fields = ('name','is_del')
    	list_filter =['name','is_del']

class ProductAdmin(admin.ModelAdmin):
    	list_display = ('pid','type_id','brand_id','name','weight','is_new','is_hot','is_commend','is_show','is_del','description','package_list','features','colors','sizes','create_time')
    	search_fields =('pid','type_id','brand_id','name','weight','is_new','is_hot','is_commend','is_show','is_del','description','package_list','features','colors','sizes','create_time')
    	list_filter =['pid','type_id','brand_id','name','weight','is_new','is_hot','is_commend','is_show','is_del','description','package_list','features','colors','sizes','create_time']

class SkuAdmin(admin.ModelAdmin):
    	list_display = ('product_id','color_id','sizes','delive_fee','price','stock','location','sku_img','sku_status','sku_type','sales')
    	search_fields =('product_id','color_id','sizes','delive_fee','price','stock','location','sku_img','sku_status','sku_type','sales')
    	list_filter =['product_id','color_id','sizes','delive_fee','price','stock','location','sku_img','sku_status','sku_type','sales']

class OrderAdmin(admin.ModelAdmin):
    	list_display = ('order_id','deliver_fee','total_fee','order_price','payment_way','payment_cash','delivery','is_confirm','is_pay','order_state','create_date','note','buyer_id')
    	search_fields =('order_id','deliver_fee','total_fee','order_price','payment_way','payment_cash','delivery','is_confirm','is_pay','order_state','create_date','note','buyer_id')
    	list_filter =['order_id','deliver_fee','total_fee','order_price','payment_way','payment_cash','delivery','is_confirm','is_pay','order_state','create_date','note','buyer_id']

class OrderdetailAdmin(admin.ModelAdmin):
    	list_display = ('order_id', 'product_id','product_name','color','size','price','amount')
    	search_fields = ('order_id', 'product_id','product_name','color','size','price','amount')
    	list_filter =['order_id', 'product_id','product_name','color','size','price','amount']

admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Producttype,ProducttypeAdmin)
admin.site.register(Productfeature,ProductfeatureAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Img,ImgAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Sku,SkuAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(Orderdetail,OrderdetailAdmin)