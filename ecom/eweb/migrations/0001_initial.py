# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=80)),
                ('img_url', models.CharField(max_length=80)),
                ('is_display', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u6027\u522b', choices=[(b'0', b'\xe4\xbf\x9d\xe5\xaf\x86'), (b'1', b'\xe7\x94\xb7'), (b'2', b'\xe5\xa5\xb3')])),
                ('register_time', models.DateTimeField(auto_now_add=True)),
                ('real_name', models.CharField(max_length=20, blank=True)),
                ('province', models.CharField(max_length=20, blank=True)),
                ('city', models.CharField(max_length=20, blank=True)),
                ('town', models.CharField(max_length=20, blank=True)),
                ('addr', models.CharField(max_length=80, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=20)),
                ('parent_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.ImageField(upload_to=b'productimages')),
                ('is_def', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.IntegerField(serialize=False, primary_key=True)),
                ('deliver_fee', models.IntegerField()),
                ('total_fee', models.FloatField()),
                ('order_price', models.FloatField()),
                ('payment_way', models.CharField(max_length=10)),
                ('payment_cash', models.CharField(max_length=10)),
                ('delivery', models.DateField(auto_now_add=True)),
                ('is_confirm', models.CharField(max_length=10)),
                ('is_pay', models.CharField(max_length=10)),
                ('order_state', models.CharField(max_length=10)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(max_length=100)),
                ('buyer_id', models.ForeignKey(to='eweb.Buyer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Orderdetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_id', models.IntegerField()),
                ('product_name', models.CharField(max_length=80)),
                ('color', models.CharField(max_length=5)),
                ('size', models.CharField(max_length=5)),
                ('price', models.FloatField()),
                ('amount', models.IntegerField(default=1)),
                ('order_id', models.ForeignKey(to='eweb.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('pid', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('weight', models.FloatField()),
                ('is_new', models.BooleanField(default=True)),
                ('is_hot', models.BooleanField(default=True)),
                ('is_commend', models.BooleanField(default=False)),
                ('is_show', models.BooleanField(default=False)),
                ('is_del', models.BooleanField(default=True)),
                ('description', models.ImageField(upload_to=b'productimages')),
                ('package_list', models.CharField(max_length=100)),
                ('features', models.CharField(max_length=100)),
                ('colors', models.CharField(max_length=100)),
                ('sizes', models.CharField(max_length=100)),
                ('create_time', models.DateTimeField()),
                ('brand_id', models.ForeignKey(to='eweb.Brand')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Productfeature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('is_del', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Producttype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('parent_id', models.IntegerField()),
                ('note', models.CharField(max_length=50)),
                ('is_display', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sku',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sizes', models.CharField(max_length=5)),
                ('delive_fee', models.IntegerField(default=10)),
                ('price', models.FloatField()),
                ('stock', models.IntegerField()),
                ('location', models.CharField(max_length=50)),
                ('sku_img', models.ImageField(upload_to=b'productimages')),
                ('sku_status', models.BooleanField(default=False)),
                ('sku_type', models.BooleanField(default=True)),
                ('sales', models.IntegerField()),
                ('color_id', models.ForeignKey(to='eweb.Color')),
                ('product_id', models.ForeignKey(to='eweb.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='type_id',
            field=models.ForeignKey(to='eweb.Producttype'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='img',
            name='product_id',
            field=models.ForeignKey(to='eweb.Product'),
            preserve_default=True,
        ),
    ]
