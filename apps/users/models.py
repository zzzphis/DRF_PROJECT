from django.contrib.auth.models import User
from django.db import models

from utils.modelMaxin import ModelSetMixin


# Create your models here.
class UserDetail(ModelSetMixin):
    SEX_CHOICES = (
        (0, '女'),
        (1, '男')
    )
    avatar = models.TextField(null=True, blank=True, verbose_name='头像')
    sex = models.IntegerField(verbose_name='性别', null=True, blank=True,
                              choices=SEX_CHOICES)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    phone = models.CharField(verbose_name='手机号码', null=True, blank=True, max_length=11, unique=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
