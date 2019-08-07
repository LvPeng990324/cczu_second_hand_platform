from django.urls import path, re_path
from . import views
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    # 用户注册路由
    path('register/', views.user_register, name='register'),
    path('register_process/', views.user_register_process, name='user_register_process'),

    # 用户登录路由
    path('login/', views.user_login, name='login'),
    path('login_process/', views.user_login_process, name='user_login_process'),

    # 商品上传路由
    path('goods_upload/', views.goods_upload, name='goods_upload'),
    path('goods_upload_process/', views.goods_upload_process, name='goods_upload_process'),

    # 显示用户路由
    path('show_user/', views.show_user, name='show_user'),

    # 展示商品详情路由
    path('show_good_details/<goods_id>', views.show_good_details, name='show_good_details'),

    # 用户登出路由
    path('user_logout/', views.user_logout, name='user_logout'),

    # 用户删除商品路由
    path('del_goods/<goods_id>', views.del_goods, name='del_goods'),

    # 用户信息修改路由
    path('user_change/', views.user_change, name='user_change'),
    path('user_change_process/', views.user_change_process, name='user_change_process'),

    # 商品信息修改路由
    path('goods_change/<goods_id>', views.goods_change, name='goods_change'),
    path('goods_change_process/<goods_id>', views.goods_change_process, name='goods_change_process'),

    # 主页界面路由
    path('', views.turn_index, name='index'),
    path('index/', views.turn_index, name='index'),
    path('index/<str:goods_category>', views.index, name='index'),

    # 添加商品评价路由
    path('goods_comment_process/<goods_id>', views.goods_comment_process, name='goods_comment_process'),

    # 查看大图路由
    path('show_big_img/<goods_id>', views.show_big_img, name='show_big_img'),

    # 待开发路由
    path('coming_soon/', views.coming_soon, name='coming_soon'),

    # 赞赏界面路由
    path('appreciate/', views.appreciate, name='appreciate'),

    # 定义图片url
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),


]
