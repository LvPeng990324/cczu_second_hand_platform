# Generated by Django 2.2.2 on 2019-07-20 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userName', models.CharField(max_length=20, verbose_name='用户名')),
                ('password', models.CharField(max_length=20, verbose_name='密码')),
                ('qq_num', models.CharField(max_length=15, verbose_name='QQ号')),
                ('sex', models.CharField(max_length=3, verbose_name='性别')),
            ],
        ),
    ]