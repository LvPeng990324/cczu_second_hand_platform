# 部署时候把注释的路径切换下
import multiprocessing

bind = "127.0.0.1:8080"
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
daemon = True
# errorlog = '/root/workplace/cczu_second_hand_platform/logs/gunicorn_error.log'
errorlog = '/home/lvpeng/workplace/django/cczu_second_hand_platform/logs/gunicorn_error.log'
proc_name = 'gunicorn_second_hand_platform_project'
