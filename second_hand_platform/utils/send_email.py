from django.conf import settings
from django.core.mail import send_mail


# 发送注册确认码邮件，参数：接收人，验证码，用户名
def send_email_register(to_email, code, user_name):
    subject = '常大东东注册验证码'
    context = '欢迎注册常大东东~' \
                   '\n' \
                   '你的验证码为{}' \
                   '\n' \
                   '请进入 {}/email_confirm/{} 输入验证码来激活你的账户~' \
                   '\n' \
                   '遇到问题的话请联系作者：lvpeng990324@163.com'.format(
        code,
        settings.SITE_URL,
        user_name,
    )
    send_mail(subject, context, settings.EMAIL_HOST_USER, [to_email])


# 发送邮箱修改确认码邮件，参数：接收人，验证码，用户名
def send_email_change_email(to_email, code, user_name):
    subject = '常大东东激活验证码'
    context = '你已经成功修改了你的邮箱~' \
                   '\n' \
                   '你的验证码为{}' \
                   '\n' \
                   '请进入 {}/email_confirm/{} 输入验证码来激活你的账户~' \
                   '\n' \
                   '遇到问题的话请联系作者：lvpeng990324@163.com'.format(
        code,
        settings.SITE_URL,
        user_name,
    )
    send_mail(subject, context, settings.EMAIL_HOST_USER, [to_email])


# 发送找回密码邮件，参数：接收人，密码
def send_email_password(to_email, password):
    subject = '常大东东密码找回'
    context = '你的密码是{} ，请妥善保管。'.format(password)
    send_mail(subject, context, settings.EMAIL_HOST_USER, [to_email])
