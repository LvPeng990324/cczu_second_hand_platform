from django.shortcuts import render, HttpResponse, redirect
from .models import User
from .models import Goods
from .models import Advertisement
from .models import GoodsComment
from .models import GoodsCategory
from django.db.utils import IntegrityError
from django.db.models import ObjectDoesNotExist

# Create your views here.


# 用户注册页面
def user_register(request):
    # 验证是否已经登录
    if request.session.get('is_login', None):
        # 已经登录的直接重定向
        return redirect('/show_user/')
    # 未登录的进入注册界面
    return render(request, 'user_login_or_register.html')


# 用户登录界面
def user_login(request):
    # 验证是否已经登录
    if request.session.get('is_login', None):
        # 已经登录的直接重定向
        return redirect('/show_user/')
    # 未登录的进入登录界面
    return render(request, 'user_login_or_register.html')


# 商品上传界面
def goods_upload(request):
    # 验证是否未登录
    if not request.session.get('is_login', None):
        # 未登录的话重定向到登录界面
        return redirect('/login/')
    # 已经登录的正常引导商品上传界面
    user_name = request.session['user_name']
    try:
        # 获取用户qq号，用于自动填写初始联系方式
        qq_num = User.objects.get(user_name=user_name).qq_num
    except:
        # 如果获取qq失败，报错并引导用户重新登录
        # 清除session记录
        request.session.flush()
        # 打包错误信息
        context = {
            'error_message_title': '你的登录出错啦~',
            'error_message_context': '重试一次或者退出登录重新登录一次试试，如果解决不了请联系作者。',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 尝试获取商品分类信息
    try:
        goods_category = GoodsCategory.objects.all()
    except:
        # 如果获取失败返回数据库错误信息
        # 打包错误信息
        context = {
            'error_message_title': '数据库出现了未知错误~',
            'error_message_context': '数据库不知道啥情况，分类读取不出来了，重新刷新试试，如果解决不了请联系作者。',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 打包qq以及商品分类信息
    context = {
        'qq_num': qq_num,
        'goods_category': goods_category,
    }
    # 引导商品上传界面，并把qq号传入页面，用于自动填写联系方式,以及传入商品分类信息
    return render(request, 'goods_upload.html', context=context)


# 用户信息修改界面
def user_change(request):
    # 验证是否未登录
    if not request.session.get('is_login', None):
        # 未登录的话重定向到登录界面
        return redirect('/login/')
    # 已经登录的正常引导用户信息修改界面
    # 获取此用户所有信息
    # 如果获取不到返回登录错误提示
    try:
        user = User.objects.get(user_name=request.session['user_name'])
    except:
        # 返回登录错误提示
        # 清除session记录
        request.session.flush()
        # 打包错误信息
        context = {
            'error_message_title': '你的登录出错啦~',
            'error_message_context': '重试一次或者退出登录重新登录一次试试，如果解决不了请联系作者。',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 打包用户信息数据
    context = {
            'user_name': user.user_name,
            'qq_num': user.qq_num,
        }
    # 引导信息修改界面，并把用户当前信息传到页面
    return render(request, 'user_change.html', context=context, )


# 商品信息修改界面
def goods_change(request, goods_id):
    # 验证是否未登录
    if not request.session.get('is_login', None):
        # 未登录的话重定向到登录界面
        return redirect('/login/')
    # 已经登录的正常引导商品信息修改界面
    # 获取此商品的信息
    # 获取不到返回商品信息错误提示
    try:
        good = Goods.objects.get(id=goods_id)
    except:
        # 返回商品信息未找到错误
        # 打包错误信息
        context = {
            'error_message_title': '你要找的商品没找到~',
            'error_message_context': '它有可能被删除了或者出现了其它未知的错误，重试一次，解决不了的话联系作者',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 尝试获取商品分类信息
    try:
        goods_category = GoodsCategory.objects.all()
    except:
        # 如果获取失败返回数据库错误信息
        # 打包错误信息
        context = {
            'error_message_title': '数据库出现了未知错误~',
            'error_message_context': '数据库不知道啥情况，分类读取不出来了，重新刷新试试，如果解决不了请联系作者。',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 检查是否是此用户上传的商品，防止修改url进行攻击的行为
    if good.user_name != request.session.get('user_name', None):
        # 如果此商品对应的用户名与此用户不符，即此用户没有权限修改此商品信息
        # 返回无权限错误
        return HttpResponse('不是你上传的商品，你无权限修改它，请不要尝试攻击行为！')
    # 没问题就打包商品以及商品分类信息数据
    context = {
        'goods_name': good.goods_name,
        'goods_price': good.goods_price,
        'comments': good.comments,
        'contact': good.contact,
        'goods_img': good.goods_img,
        'goods_id': good.id,
        'goods_category': goods_category,
    }
    # 引导信息修改界面，并把商品信息传到页面
    return render(request, 'goods_change.html', context=context)


# 主页界面
def index(request, goods_category):
    # 判断商品分类是否是*
    if goods_category == '*':
        # 如果是#
        # 获取所有商品信息
        # 倒序获取商品，保持最新发布的商品在前边
        goods = Goods.objects.all()[::-1]
        # 把goods_category重新赋值为最新发布，方便在主页显示类别
        goods_category = '最新发布'
    else:
        # 如果不是#
        # 筛选出该类别的商品
        # 倒序获取商品，保持最新发布的商品在前边
        goods = Goods.objects.filter(goods_category=goods_category)[::-1]
    # 获取所有广告信息
    advertisements = Advertisement.objects.all()
    # 获取所有商品分类信息
    goods_category_list = GoodsCategory.objects.all()
    # 打包所有商品和广告信息
    # 因为广告滑动区第一个元素与其他元素的class属性需不同，所以这里单独把第一个广告信息拿出来
    # advertisements_num_array是为了配合生成广告下边滑动点点的数组
    context = {
        'goods': goods,
        'goods_category': goods_category,
        'goods_category_list': goods_category_list,
        'advertisements': advertisements[1:],
        'first_advertisement': advertisements[0],
        'advertisements_num_array': range(1, len(advertisements))
    }
    # 引导主页界面并传入打包数据
    return render(request, 'index.html', context=context)


# 查看大图界面
def show_big_img(request, goods_id):
    # 先检查此时商品还在不在
    # 尝试读取商品图片
    try:
        goods_img = Goods.objects.get(id=goods_id).goods_img
    except:
        # 如果此时此商品已不存在了，返回此商品已不存在错误
        # 打包错误信息
        context = {
            'error_message_title': '你要查看的商品已经不存在啦~',
            'error_message_context': '真凑巧！可能就在你要评论的时候此商品被删除了，刷新下看看它是否还在。',
        }
        # 引导404界面并把错误信息传入404
        return render(request, '404.html', context=context)
    # 没问题就引导大图界面并将大图路径传入界面
    # 打包图片信息
    context = {
        'goods_img': goods_img,
    }
    return render(request, 'show_big_img.html', context=context)


# 将可能是访问主页的请求重定向到主页最新发布
def turn_index(request):
    return redirect('index', '*')


# 待开发界面
def coming_soon(request):
    return render(request, 'coming_soon.html')


# 赞赏界面
def appreciate(request):
    return render(request, 'appreciate.html')


########################################################################
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~以上是界面区域~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 我是一条骚骚的~~~~~~~~~~~~~~~~界面与逻辑分界线~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~以下是逻辑区域~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
########################################################################


# 用户注册逻辑
def user_register_process(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        qq_num = request.POST.get('qq_num')

        # 判断两次输入密码是否相同
        if password_1 != password_2:
            # 如果不相同，返回两次密码不匹配错误
            # 打包错误信息
            context = {
                'error_message_register': '两次密码不匹配！'
            }
            # 引导登录界面并将错误信息传入
            return render(request, 'user_login_or_register.html', context=context)

        try:
            User.objects.get_or_create(
                user_name=user_name,
                password=password_1,
                qq_num=qq_num,
            )
        except IntegrityError:
            # 返回用户名已被注册错误提示
            # 打包错误信息
            context = {
                'error_message_register': '此用户名已被注册！'
            }
            # 引导登录界面并将错误信息传入
            return render(request, 'user_login_or_register.html', context=context)
    else:
        return render(request, 'user_login_or_register.html')
    # 打包成功信息
    context = {
        'success_message_title': '注册成功~',
        'success_message_context': '恭喜你成功注册了一个账号，请发布真实的商品，不要存在欺骗行为，商品卖出后记得及时删除，OK，快去登录吧~',
        'success_message_button': '前往登录',
        'success_url': 'login',
    }
    # 引导注册成功界面
    return render(request, 'success.html', context=context)


# 用户登录逻辑
def user_login_process(request):
    # 用户登录流程
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        # 检查用户名是否存在
        login_name = User.objects.filter(user_name=user_name)
        if login_name:
            if password == login_name[0].password:
                # 登陆成功，将信息写入session
                request.session['is_login'] = True
                request.session['user_name'] = user_name
                # 重定向到登录成功页面
                # return render(request, 'show_user.html')
                return redirect('/show_user/')
            else:
                # 返回密码错误提示
                # 打包错误信息
                context = {
                    'error_message_login': '密码错误！'
                }
                # 引导登录界面并将错误信息传入
                return render(request, 'user_login_or_register.html', context=context)
        else:
            # 返回用户名不存在错误提示
            # 打包错误信息
            context = {
                'error_message_login': '用户名不存在！'
            }
            # 引导登录界面并将错误信息传入
            return render(request, 'user_login_or_register.html', context=context)
    else:
        return render(request, 'user_login_or_register.html')


# 商品上传逻辑
def goods_upload_process(request):
    if request.method == 'POST':
        goods_img = request.FILES.get('goods_img')
        goods_name = request.POST.get('goods_name')
        goods_price = request.POST.get('goods_price')
        comments = request.POST.get('comments')
        contact = request.POST.get('contact')
        goods_category = request.POST.get('goods_category')
        user_name = request.session['user_name']

        try:
            Goods.objects.get_or_create(
                goods_img=goods_img,
                goods_name=goods_name,
                goods_price=goods_price,
                comments=comments,
                contact=contact,
                user_name=user_name,
                goods_category=goods_category,
            )
        except:
            # return HttpResponse('未知错误！')
            # 返回数据库未知错误
            # 打包错误信息
            context = {
                'error_message_title': '发生了很神奇的错误~',
                'error_message_context': '我不清楚发生了啥错误，看上去像是数据库出错了，请先检查你填写的内容有无极端情况，解决不了的话联系作者。',
            }
            # 引导404界面并把错误信息传入404
            return render(request, '404.html', context=context)
    else:
        return render(request, 'goods_upload.html')
    # 打包成功信息
    context = {
        'success_message_title': '上传成功~',
        'success_message_context': '恭喜你成功上传了一件商品，快去你的个人信息界面看看吧~',
        'success_message_button': '前往我的',
        'success_url': 'show_user',
    }
    # 引导个人信息界面
    return render(request, 'success.html', context=context)


# 返回用户信息
def show_user(request):
    # 验证是否未登录
    if not request.session.get('is_login', None):
        # 未登录的话重定向到登录界面
        return redirect('/login/')
    # 已经登录的正常引导显示信息界面
    try:
        # 获取此用户注册信息
        user = User.objects.get(user_name=request.session['user_name'])
        # 获取此用户发布的所有商品信息
        goods_list = Goods.objects.filter(user_name=request.session['user_name'])
    except:
        # 返回登录错误提示
        # 清除session记录
        request.session.flush()
        # 打包错误信息
        context = {
            'error_message_title': '你的登录出错啦~',
            'error_message_context': '重试一次或者退出登录重新登录一次试试，如果解决不了请联系作者。',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 打包用户信息数据
    context = {
        'user_name': user.user_name,
        'qq_num': user.qq_num,
        'password': user.password,
        'goods_list': goods_list,
    }
    # 引导用户信息界面，并把用户数据传入页面
    return render(request, 'show_user.html', context=context)


# 展示商品详情
def show_good_details(request, goods_id):
    # 获取此商品的所有信息
    try:
        good_details = Goods.objects.get(id=goods_id)
    except:
        # 如果找不到则返回商品未找到错误
        # 打包错误信息
        context = {
            'error_message_title': '你要找的商品没找到~',
            'error_message_context': '它有可能被删除了或者出现了其它未知的错误，重试一次，解决不了的话联系作者',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 尝试获取关于此商品的评论信息
    try:
        comments = GoodsComment.objects.filter(goods_id=goods_id)
    except:
        # 如果出错就把comments置空（想不出会出什么错。。。）
        comments = ()
    # 打包商品信息和评论信息
    context = {
        'good_details': good_details,
        'comments': comments,
    }
    # 将信息变量传到网页中
    return render(request, 'show_good_details.html', context=context)


# 用户登出
def user_logout(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    request.session.flush()
    # 打包成功信息
    context = {
        'success_message_title': '登出成功~',
        'success_message_context': '成功退出当前账号，快去登录另一个吧~',
        'success_message_button': '前往登录',
        'success_url': 'login',
    }
    # 引导注册成功界面
    return render(request, 'success.html', context=context)


# 用户删除商品
def del_goods(request, goods_id):
    # 尝试删除该商品以及关于它的评论
    try:
        Goods.objects.get(id=goods_id).delete()
        GoodsComment.objects.filter(goods_id=goods_id).delete()
    except:
        # 返回商品信息未找到错误
        # 打包错误信息
        context = {
            'error_message_title': '你要删除的商品没找到~',
            'error_message_context': '它有可能被删除了或者出现了其它未知的错误，重试一次，解决不了的话联系作者',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 删除成功重定向回用户信息界面
    return redirect('show_user')


# 用户信息修改逻辑
def user_change_process(request):
    # 获取用户信息
    try:
        user = User.objects.get(user_name=request.session['user_name'])
    except:
        # 获取不到返回登录错误提示
        # 清除session记录
        request.session.flush()
        # 打包错误信息
        context = {
            'error_message_title': '你的登录出错啦~',
            'error_message_context': '重试一次或者退出登录重新登录一次试试，如果解决不了请联系作者。',
        }
        # 引导404界面并将错误信息传入404
        return render(request, '404.html', context=context)
    # 验证用户输入的密码正确性
    if user.password == request.POST.get('password'):
        # 没问题就获取修改值并更新信息
        if request.method == 'POST':
            # 判断是否输入了新密码：
            new_password_1 = request.POST.get('new_password_1')
            new_password_2 = request.POST.get('new_password_2')
            if new_password_1 or new_password_2:
                # 如果输入了，判断是否相同
                if new_password_2 == new_password_1:
                    # 如果相同就令新密码更新
                    new_password = new_password_1
                else:
                    # 如果不相同就返回两次密码 不同错误
                    # 打包错误信息以及用户信息
                    context = {
                        'error_message': '两次输入的新密码不同！',
                        'user_name': user.user_name,
                        'qq_num': user.qq_num,
                    }
                    # 引导修改信息界面，并将信息传入
                    return render(request, 'user_change.html', context=context)
            else:
                # 如果没有输入新密码就让新密码等于旧密码
                new_password = user.password
            # 获取信息并更新数据库
            user.qq_num = request.POST.get('qq_num')
            user.password = new_password
            user.save()
            # 打包成功信息
            context = {
                'success_message_title': '修改成功~',
                'success_message_context': '恭喜你成功修改了你的信息，回到自己的信息页面看看吧~',
                'success_message_button': '前往我的',
                'success_url': 'show_user',
            }
            # 引导个人信息界面
            return render(request, 'success.html', context=context)
        else:
            # 重定向到用户信息修改界面
            return redirect('user_change')
    else:
        # 如果输入密码错误，返回密码错误提示
        # 打包错误信息以及用户信息
        context = {
            'error_message': '输入的密码有误！',
            'user_name': user.user_name,
            'qq_num': user.qq_num,
        }
        # 引导修改信息界面，并将信息传入
        return render(request, 'user_change.html', context=context)


# 商品信息修改逻辑
def goods_change_process(request, goods_id):
    if request.method == 'POST':
        # 获取商品信息
        try:
            good = Goods.objects.get(id=goods_id)
        except:
            # 获取不到返回商品信息获取错误提示
            # 打包错误信息
            context = {
                'error_message_title': '你要找的商品没找到~',
                'error_message_context': '它有可能被删除了或者出现了其它未知的错误，重试一次，解决不了的话联系作者',
            }
            # 引导404界面并将错误信息传入404
            return render(request, '404.html', context=context)
        # 没问题就获取修改值并更新信息
        # 判断用户是否上传了图片
        if request.FILES.get('goods_img'):
            # 如果上传了则替换为新图片
            good.goods_img = request.FILES.get('goods_img')
        else:
            # 如果没上传则不对图片进行操作
            pass
        # 继续获取并更新其他信息
        good.goods_name = request.POST.get('goods_name')
        good.goods_price = request.POST.get('goods_price')
        good.contact = request.POST.get('contact')
        good.comments = request.POST.get('comments')
        good.goods_category = request.POST.get('goods_category')
        # 保存更改
        good.save()
        # 提示成功
        # 打包成功信息
        context = {
            'success_message_title': '修改成功~',
            'success_message_context': '恭喜你成功修改了这个商品的信息，回到自己的信息页面看看吧~',
            'success_message_button': '前往我的',
            'success_url': 'show_user',
        }
        # 引导个人信息界面
        return render(request, 'success.html', context=context)
    else:
        # 重定向到商品信息修改界面
        return redirect('goods_change')


# 添加商品评价逻辑
def goods_comment_process(request, goods_id):
    # 验证是否未登录
    if not request.session.get('is_login', None):
        # 未登录的话重定向到登录界面
        return redirect('/login/')
    # 已经登录的正常获取评论内容以及被评论商品ID
    if request.method == 'POST':
        # 获取评论内容
        comment = request.POST.get('comment')
        # 尝试获取用户名
        try:
            user_name = request.session['user_name']
        except:
            # 如果获取用户名失败，则返回登录失败错误
            # 清除session记录
            request.session.flush()
            # 打包错误信息
            context = {
                'error_message_title': '你的登录出错啦~',
                'error_message_context': '重试一次或者退出登录重新登录一次试试，如果解决不了请联系作者。',
            }
            # 引导404界面并将错误信息传入404
            return render(request, '404.html', context=context)
        # 尝试将评论数据写入数据库
        try:
            # 检查此时该商品是否存在
            try:
                Goods.objects.get(id=goods_id)
            except ObjectDoesNotExist:
                # 如果此时此商品已不存在了，返回此商品已不存在错误
                # 打包错误信息
                context = {
                    'error_message_title': '你要评论的商品已经不存在啦~',
                    'error_message_context': '真凑巧！可能就在你要评论的时候此商品被删除了，刷新下看看它是否还在。',
                }
                # 引导404界面并把错误信息传入404
                return render(request, '404.html', context=context)
            # 如果商品仍然存在，则尝试写入数据库
            GoodsComment.objects.get_or_create(
                comment=comment,
                goods_id=goods_id,
                user_name=user_name,
            )
            # 评论成功后重定向回当前页面，相当于刷新
            return redirect('show_good_details', goods_id)
        except:
            # 如果写入出错，返回数据库未知错误
            # 打包错误信息
            context = {
                'error_message_title': '发生了很神奇的错误~',
                'error_message_context': '我不清楚发生了啥错误，看上去像是数据库出错了，请先检查你填写的内容有无极端情况，解决不了的话联系作者。',
            }
            # 引导404界面并把错误信息传入404
            return render(request, '404.html', context=context)
    else:
        # 重定向到404错误，提示提交失败
        # 打包错误信息
        context = {
            'error_message_title': '评论提交失败~',
            'error_message_context': '出现了未知的错误，提交协议不符合规定，请不要尝试攻击，如果你是无辜的，重试一次，解决不了的话联系作者',
        }
        # 引导404并将错误信息传入页面
        render(request, '404.html', context=context)

