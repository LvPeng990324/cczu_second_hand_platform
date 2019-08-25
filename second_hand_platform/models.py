from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField

# Create your models here.


# 用户信息
class User(models.Model):
    user_name = models.CharField(max_length=20, verbose_name='用户名', primary_key=True)
    password = models.CharField(max_length=20, verbose_name='密码')
    qq_num = models.CharField(max_length=15, verbose_name='QQ号')
    email = models.EmailField(verbose_name='邮箱')
    confirmed = models.BooleanField(verbose_name='是否确认邮箱', default=False)
    code = models.CharField(max_length=10, verbose_name='邮箱验证码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


# 商品分类
class GoodsCategory(models.Model):
    goods_category = models.CharField(max_length=10, verbose_name='商品分类', primary_key=True)

    def __str__(self):
        return self.goods_category

    class Meta:
        verbose_name_plural = '商品分类'
        verbose_name = '商品分类'


# 商品信息
class Goods(models.Model):
    goods_name = models.CharField(max_length=100, verbose_name='商品名称')
    user_name = models.CharField(max_length=20, verbose_name='用户名')
    goods_price = models.FloatField(verbose_name='商品价格')
    comments = models.TextField(verbose_name='商品介绍')
    contact = models.CharField(max_length=100, verbose_name='联系方式')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='上架时间')
    goods_img = ThumbnailerImageField(upload_to='goods_img', verbose_name='商品图片')
    goods_category = models.CharField(max_length=10, verbose_name='商品分类')

    def __str__(self):
        return self.goods_name

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = '商品信息'


# 广告信息
class Advertisement(models.Model):
    big_title_orange = models.CharField(max_length=10, verbose_name='大标题橙色字')
    big_title_grey = models.CharField(max_length=10, verbose_name='大标题灰色字')
    small_title = models.CharField(max_length=30, verbose_name='小标题')
    context = models.TextField(verbose_name='内容')
    advertisement_url = models.URLField(verbose_name='广告网址')
    advertisement_img = models.ImageField(upload_to='advertisement_img', verbose_name='广告图片')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    last_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    def __str__(self):
        return '%s-%s' % (self.big_title_orange, self.big_title_grey)

    class Meta:
        verbose_name_plural = '广告信息'
        verbose_name = '广告信息'


# 商品评论
class GoodsComment(models.Model):
    comment = models.TextField(verbose_name='评论内容')
    goods_id = models.IntegerField(verbose_name='被评论商品ID')
    user_name = models.CharField(max_length=20, verbose_name='评论发布用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = '商品评论'
        verbose_name_plural = '商品评论'
