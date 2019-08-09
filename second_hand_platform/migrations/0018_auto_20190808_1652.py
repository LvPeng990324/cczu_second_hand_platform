# Generated by Django 2.2.2 on 2019-08-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('second_hand_platform', '0017_auto_20190806_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='code',
            field=models.CharField(default='', max_length=10, verbose_name='邮箱验证码'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='是否确认邮箱'),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default='', max_length=254, verbose_name='邮箱'),
            preserve_default=False,
        ),
    ]
