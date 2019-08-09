from django.contrib import admin
from .models import User
from .models import Goods
from .models import Advertisement
from .models import GoodsComment
from .models import GoodsCategory

# Register your models here.


# 注册用户信息
@admin.register(User)
class UserInformation(admin.ModelAdmin):
    list_display = ('user_name', 'password', 'qq_num', 'email', 'confirmed', 'create_time',)


# 注册商品分类信息
@admin.register(GoodsCategory)
class GoodsCategoryInformation(admin.ModelAdmin):
    pass


# 注册商品信息
@admin.register(Goods)
class GoodsInformation(admin.ModelAdmin):
    list_display = ('goods_name', 'goods_category', 'user_name', 'goods_price', 'create_time', 'id', 'goods_img',)


# 注册广告信息
@admin.register(Advertisement)
class AdvertisementInformation(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'create_time', 'last_time',)


# 注册商品评论信息
@admin.register(GoodsComment)
class GoodsCommentInformation(admin.ModelAdmin):
    list_display = ('comment', 'goods_id', 'user_name', 'create_time',)


# 注册信息到管理员
# admin.site.register(User, UserInformation)
# admin.site.register(Goods, GoodsInformation)

