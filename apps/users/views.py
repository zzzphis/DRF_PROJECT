import io

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View
from django_redis import get_redis_connection
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from config.dbs.redisconfig import KEY_TEMPLATE, EXPIRE_TIME
from users.serializers import UserSerializer, MyTokenObtainPairSerializer, UserDetailSerializer, \
    UpdatePasswordSerializer
from utils.verifyutil import ImageVerify


# Create your views here.
class ImageVerifyView(View):
    def get(self, request, uuid, func):
        imageVerify = ImageVerify()
        img, code = imageVerify.verify_code()

        # 生成一个临时文件
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # 保存到数据库
        cache = get_redis_connection(alias='verify_codes')  # 使用redis
        cache.set(KEY_TEMPLATE % (func, uuid), code, EXPIRE_TIME)  # uuid作为key，code作为value，过期时间为60秒
        print(cache.get(KEY_TEMPLATE % (func, uuid)))  # 打印缓存中的验证码
        # 返回字节数据

        return HttpResponse(img_bytes, content_type='image/png')


# GenericViewSet 没有任何默认的方法
# 视图集是用于交互
class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #
    def get_permissions(self):
        if self.action in ['now', 'info']:
            permission_classes = [IsAuthenticated]  # IsAuthenticated->> 登录权限类

        else:
            permission_classes = []
        return [permission() for permission in permission_classes]  # 返回权限对象

    # 修改个人信息需要使用UserDetailSerializer
    # 需要判断当前路由是否是info再选择是否更换序列化器
    def get_serializer_class(self):
        if self.action in ['info']:
            return UserDetailSerializer
        elif self.action in['password']:
            return UpdatePasswordSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer.is_valid())
        serializer.is_valid(raise_exception=True)

        # 得到用户传入的数据
        username = request.data.get('username')
        password = request.data.get('password')

        # 创建用户对象，并且进行持久化
        user = User(username=username)
        user.set_password(password)  # 密码加密
        user.save()

        return Response(self.get_serializer(user).data)

    @action(methods=['get'], detail=False)
    def now(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(methods=['put'], detail=False)
    def info(self, request):
        user = request.user
        # print(request.)
        # 强制的将post数据中的user与登录的用户进行匹配
        # 允许修改POST的数据
        request.POST._mutable = True
        request.data['user'] = user.id
        print(request.data)
        # 判断是否有详情数据
        if hasattr(user, 'userDetail'):
            # 如果有就修改
            user_detail_serializer = self.get_serializer(user.userDetail, data=request.data)
        else:
            user_detail_serializer = self.get_serializer(data=request.data)
        user_detail_serializer.is_valid(raise_exception=True)
        user_detail_serializer.save()
        return Response(user_detail_serializer.data)

    @action(methods=['put'], detail=False)
    def password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = request.data['oldPassword']
        new_Passowrd = request.data['newPassword']
        if user.check_password(password):
            user.set_password(new_Passowrd)
            user.save()
            return Response({'msg':'修改成功'})
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
