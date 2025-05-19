from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from config.dbs.redisconfig import KEY_TEMPLATE
from users.models import UserDetail


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(write_only=True)
    verify = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['first_name', 'last_name', 'groups', 'user_permissions', 'last_login', 'date_joined']
        extra_kwargs = {
            'is_superuser': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        uuid = attrs.get('uuid')
        verify = attrs.get('verify')
        cache = get_redis_connection(alias='verify_codes')  # 使用redis
        redis_verify = cache.get(KEY_TEMPLATE % ('register', uuid))
        cache.delete(KEY_TEMPLATE % ('register', uuid))
        if not redis_verify:
            raise serializers.ValidationError('验证码已过期')
        if redis_verify.upper() != verify.upper():
            raise serializers.ValidationError('验证码错误')
        return attrs
        # 验证码验证逻辑


# 登录
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    uuid = serializers.CharField(write_only=True)
    verify = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        验证数据
        :param attrs:
        :return:
        """
        uuid = attrs.get('uuid')
        verify = attrs.get('verify')
        username = attrs.get('username')
        password = attrs.get('password')
        cache = get_redis_connection(alias='verify_codes')
        redis_verify = cache.get(KEY_TEMPLATE % ('login', uuid))
        cache.delete(KEY_TEMPLATE % ('login', uuid))
        if not redis_verify:
            raise serializers.ValidationError('验证码已过期')
        if redis_verify.upper() != verify.upper():
            raise serializers.ValidationError('验证码错误')

        # 用户信息校验
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('用户名或密码错误')
        refresh = self.get_token(user)
        return {'user': user.username, 'token': str(refresh.access_token)}


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        exclude = ['is_delete']


class UpdatePasswordSerializer(serializers.Serializer):
    oldPassword = serializers.CharField(max_length=60, label='原密码', help_text='原密码')
    newPassword = serializers.CharField(max_length=60, label='新密码', help_text='新密码')
    re_newPassword = serializers.CharField(max_length=60, label='确认密码', help_text='确认密码')

    def validate(self, attrs):
        if attrs['newPassword'] != attrs['re_newPassword']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs
