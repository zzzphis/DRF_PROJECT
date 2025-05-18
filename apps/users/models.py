from django.contrib.auth.models import User
from django.db import models

from utils.modelMaxin import ModelSetMixin


# Create your models here.
class UserDetail(ModelSetMixin):
    sex_choice = {
        (1, '男'),
        (2, '女')
    }
    avator = models.TextField(max_length=30, verbose_name='头像', null=True)
    sex = models.IntegerField(verbose_name='性别', null=True, blank=True,
                              choices=sex_choice)
    birthday = models.DateTimeField(verbose_name='生日', null=True, blank=True)
    age = models.IntegerField(verbose_name='年龄', null=True, blank=True)
    phone = models.CharField(verbose_name='手机号码', null=True, blank=True, max_length=11, unique=True)
    # 相当于为user设置一个新的字段这个字段中的数据是userDetail对象数据
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userDetail')
